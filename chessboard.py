import chess
import mysql.connector

class ChessGame:
    def __init__(self):
        # Connect to your MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="maggie",
            database="chessboard"
        )
        self.cursor = self.connection.cursor()

        # Initialize a new chess board in python-chess
        self.board = chess.Board()

        # Load the current state of the board from the database
        self.load_board_from_db()

    def load_board_from_db(self):
        """Load the chessboard state from the MySQL database."""
        # Fetch all pieces and their positions
        self.cursor.execute("SELECT `column`, `row`, piece, `empty` FROM chess")
        rows = self.cursor.fetchall()

        # Reset python-chess board
        self.board.clear()

        for row in rows:
            col, row, piece, empty = row

            if not empty and piece:
                # Convert database position into python-chess position
                chess_pos = chess.square(ord(col.lower()) - ord('a'), int(row) - 1)

                # Map piece to python-chess format (e.g., 'WQ' -> chess.QUEEN)
                color = chess.WHITE if piece[0] == 'W' else chess.BLACK
                piece_type = self.get_piece_type(piece[1])
                
                # Place the piece on the python-chess board
                self.board.set_piece_at(chess_pos, chess.Piece(piece_type, color))

    def get_piece_type(self, piece_char):
        """Return the chess piece type based on the character."""
        return {
            'R': chess.ROOK,
            'N': chess.KNIGHT,
            'B': chess.BISHOP,
            'Q': chess.QUEEN,
            'K': chess.KING,
            'P': chess.PAWN
        }.get(piece_char, None)

    def display_board(self):
        """Print a text representation of the chessboard."""
        print(self.board)

    def update_board(self, from_pos, to_pos):
        """Attempt to move a piece from `from_pos` to `to_pos`."""
        from_square = f"{chr(from_pos[1] + ord('a'))}{from_pos[0] + 1}"
        to_square = f"{chr(to_pos[1] + ord('a'))}{to_pos[0] + 1}"
        
        move_str = f"{from_square}{to_square}"  # Convert to UCI format (e.g., "e2e4")
        move = chess.Move.from_uci(move_str)

        # Validate the move using python-chess
        if move in self.board.legal_moves:
            self.board.push(move)  # Apply the move to the python-chess board
            print(f"Move {move_str} made.")

            # Update the database to reflect the new board state
            self.update_database(from_pos, to_pos)
        else:
            print("Illegal move!")

    def update_database(self, from_pos, to_pos):
        """Update the MySQL database to reflect the chess move."""
        # Convert positions to database format
        from_col = chr(from_pos[1] + ord('A'))
        from_row = from_pos[0] + 1
        to_col = chr(to_pos[1] + ord('A'))
        to_row = to_pos[0] + 1

        # Fetch the piece from the 'from' position in the database
        self.cursor.execute(
            "SELECT piece FROM chess WHERE `column` = %s AND `row` = %s",
            (from_col, from_row)
        )
        piece = self.cursor.fetchone()[0]  # Get the piece to move

        # Clear the 'from' position
        self.cursor.execute(
            "UPDATE chess SET piece = NULL, `empty` = TRUE WHERE `column` = %s AND `row` = %s",
            (from_col, from_row)
        )

        # Set the 'to' position
        self.cursor.execute(
            "UPDATE chess SET piece = %s, `empty` = FALSE WHERE `column` = %s AND `row` = %s",
            (piece, to_col, to_row)
        )

        # Commit the changes to the database
        self.connection.commit()

    def is_check(self):
        """Check if the current player is in check."""
        return self.board.is_check()

    def is_checkmate(self):
        """Check if the current player is in checkmate."""
        return self.board.is_checkmate()

    def is_stalemate(self):
        """Check if the game is in a stalemate."""
        return self.board.is_stalemate()

# Example Usage

# Initialize the game
game = ChessGame()

# Display the current board
game.display_board()

# Attempt to make a move (e.g., move the piece from e2 to e4)
game.update_board((1, 4), (3, 4))  # e2 to e4 in 0-indexed format

# Display the updated board
game.display_board()

# Check if it's check or checkmate
if game.is_check():
    print("Check!")
if game.is_checkmate():
    print("Checkmate!")
if game.is_stalemate():
    print("Stalemate!")
