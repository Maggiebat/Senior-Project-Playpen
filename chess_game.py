import tkinter as tk
from tkinter import messagebox
import chess
import chess.engine
import mysql.connector
import time

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game with AI")
        
        # Chess board size
        self.board_size = 8
        self.square_size = 64  # Size of each square in pixels
        
        # Initialize MySQL database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="maggie",  # Replace with your MySQL password
            database="chessboard"
        )
        self.cursor = self.connection.cursor()

        # Initialize python-chess board
        self.board = chess.Board()

        # Create Canvas to draw chessboard
        self.canvas = tk.Canvas(self.root, width=self.board_size * self.square_size, 
                                height=self.board_size * self.square_size)
        self.canvas.pack()

        # Load piece images
        self.piece_images = self.load_piece_images()

        # Draw the chessboard
        self.draw_board()

        # Place pieces on the board
        self.update_pieces()

        # Bind click events to the board
        self.canvas.bind("<Button-1>", self.on_square_click)

        # Creates a button that prints the board state **debug feature**
        print_button = tk.Button(self.root, text="Print Board State", command=self.print_board_state)
        print_button.pack()

        # Makes it so you can hit Escape to leave the game
        self.root.bind("<Escape>", lambda event: self.quit_game())

        # Track selected square and moves
        self.selected_square = None

        # Turn-based logic
        self.is_player_turn = True  # Player starts

        # Initialize Stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\Maggi\\OneDrive\\Documents\\UMASSD\\Fall24\\CIS 498\\Senior Project Playpen\\stockfish-windows-x86-64-avx2.exe")

    def quit_game(self):
        # Resets the SQL table
        self.reset_board()
        # Close the Stockfish engine
        self.engine.quit()
        # Close the MySQL connection
        self.connection.close()
        # Close the GUI window
        self.root.quit()
        print("Game ended")

    def reset_board(self):
        # Delete all existing rows in the chess table
        self.cursor.execute("TRUNCATE TABLE chess")

        # Repopulate the table with the initial chessboard setup and set visible to TRUE
        initial_setup = [
            ('A', 1, 'WR1', False, True), ('B', 1, 'WN', False, True), ('C', 1, 'WB', False, True),
            ('D', 1, 'WQ', False, True), ('E', 1, 'WK', False, True), ('F', 1, 'WB', False, True),
            ('G', 1, 'WN', False, True), ('H', 1, 'WR2', False, True),
            ('A', 2, 'WP1', False, True), ('B', 2, 'WP2', False, True), ('C', 2, 'WP3', False, True),
            ('D', 2, 'WP4', False, True), ('E', 2, 'WP5', False, True), ('F', 2, 'WP6', False, True),
            ('G', 2, 'WP7', False, True), ('H', 2, 'WP8', False, True),
            # Black pieces setup
            ('A', 8, 'BR1', False, True), ('B', 8, 'BN', False, True), ('C', 8, 'BB', False, True),
            ('D', 8, 'BQ', False, True), ('E', 8, 'BK', False, True), ('F', 8, 'BB', False, True),
            ('G', 8, 'BN', False, True), ('H', 8, 'BR2', False, True),
            ('A', 7, 'BP1', False, True), ('B', 7, 'BP2', False, True), ('C', 7, 'BP3', False, True),
            ('D', 7, 'BP4', False, True), ('E', 7, 'BP5', False, True), ('F', 7, 'BP6', False, True),
            ('G', 7, 'BP7', False, True), ('H', 7, 'BP8', False, True)
        ]

        query = "INSERT INTO chess (`column`, `row`, `piece`, `empty`, `visible`) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.executemany(query, initial_setup)
        self.connection.commit()

        print("Board has been reset to initial state with all pieces visible.")


    # Loads the photos so that the GUI has chess pieces on the board
    def load_piece_images(self):
        """Load piece images from files (you can use any chess piece images here)."""
        pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
        piece_images = {}
        for piece in pieces:
            piece_images[piece] = tk.PhotoImage(file=f"images/{piece}.png")
        return piece_images

    def draw_board(self):
        """Draw the chessboard on the canvas."""
        colors = ["#f5ffff", "#363838"]  # Light and dark squares
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def update_pieces(self):
        """Place pieces on the board according to the current board state."""
        # Clear all existing pieces from the board
        self.canvas.delete("piece")

        # Place pieces on the board
        for row in range(8):
            for col in range(8):
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_str = piece.symbol().lower() if piece.color else piece.symbol().upper()
                    image = self.piece_images.get(f"{'w' if piece.color else 'b'}{piece_str.lower()}")
                    if image:
                        x = col * self.square_size
                        y = row * self.square_size
                        self.canvas.create_image(x + self.square_size // 2, y + self.square_size // 2, 
                                                 image=image, tags="piece")

    def on_square_click(self, event):
        """Handle click events to select and move pieces."""
        if not self.is_player_turn:
            return  # Disable click when it's the AI's turn

        col = event.x // self.square_size
        row = event.y // self.square_size
        clicked_square = chess.square(col, 7 - row)

        if self.selected_square is None:
            # Select the piece if any
            if self.board.piece_at(clicked_square):
                self.selected_square = clicked_square
        else:
            # Try to make a move
            move = chess.Move(self.selected_square, clicked_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_pieces()

                # Update the database
                self.update_database(self.selected_square, clicked_square)

                # Check for game-ending conditions
                if self.check_game_over():
                    return

                # Player's move is done, now AI's turn
                self.is_player_turn = False
                self.root.after(500, self.ai_move)  # Delay AI's move slightly for realism
            else:
                messagebox.showerror("Illegal Move", "That move is not legal.")

            # Reset selected square
            self.selected_square = None

    def update_database(self, from_square, to_square):
        """Update the MySQL database after a move."""
        from_col = chr(chess.square_file(from_square) + ord('A'))
        from_row = 8 - chess.square_rank(from_square)
        to_col = chr(chess.square_file(to_square) + ord('A'))
        to_row = 8 - chess.square_rank(to_square)

        # Get the piece to move
        piece = self.board.piece_at(to_square).symbol().upper()

        # Clear the 'from' position in the database
        self.cursor.execute(
            "UPDATE chess SET piece = NULL, `empty` = TRUE WHERE `column` = %s AND `row` = %s",
            (from_col, from_row)
        )

        # Set the 'to' position in the database
        self.cursor.execute(
            "UPDATE chess SET piece = %s, `empty` = FALSE WHERE `column` = %s AND `row` = %s",
            (piece, to_col, to_row)
        )

        # Commit the changes
        self.connection.commit()

    def ai_move(self):
        """Make a move for the AI using Stockfish."""
        result = self.engine.play(self.board, chess.engine.Limit(time=2.0))  # AI calculates best move
        self.board.push(result.move)
        self.update_pieces()

        # Update the database with AI move
        self.update_database(result.move.from_square, result.move.to_square)

        # Check for game-ending conditions
        if self.check_game_over():
            return

        # AI's turn is done, back to player's turn
        self.is_player_turn = True

    def check_game_over(self):
        """Check if the game is over (checkmate, stalemate, etc.)."""
        if self.board.is_checkmate():
            messagebox.showinfo("Checkmate", "Checkmate!")
            return True
        elif self.board.is_stalemate():
            messagebox.showinfo("Stalemate", "Stalemate!")
            return True
        elif self.board.is_check():
            messagebox.showinfo("Check", "Check!")
        return False
    
    def print_board_state(self):
        self.cursor.execute("SELECT * FROM chess;")
        results = self.cursor.fetchall()
        for row in results:
            print(row)

    def close(self):
        """Close the Stockfish engine and MySQL connection."""
        self.engine.quit()
        self.connection.close()

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGUI(root)
    root.protocol("WM_DELETE_WINDOW", game.close)  # Handle window close event
    root.mainloop()