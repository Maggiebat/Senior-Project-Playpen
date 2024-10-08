import tkinter as tk
import chess
import mysql.connector

db_config = {
        'user': 'root',
        'password': 'maggie',
        'host': 'localhost',
        'database': 'chessboard'
    }

class Chessboard(tk.Tk):
    def __init__(self, db_config):
        super().__init__()
        self.title("Chessboard")
        self.geometry("400x400")

        # database connection
        self.db_config = db_config
        self.connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.connection.cursor()

        # create the board
        self.create_board()
        self.load_board_state()

    def create_board(self):
        self.squares = {}
        for i in range(8):
            for j in range(8):
                color = "white" if (i+j) % 2 == 0 else "black"
                square = tk.Frame(self,bg=color, width=50, height=50)
                square.grid(row=i,column=j)
                self.squares[(i,j)] = square

    def load_board_state(self):
        self.cursor.execute("SELECT `column`, `row`, piece, `empty`, visible FROM chess ORDER BY `row`, `column`")
        pieces = self.cursor.fetchall()
        
        # Update GUI with peices from the database
        for column, row, piece, is_empty, is_visible in pieces:
            square = self.squares[(row-1, ord(column) - ord('A'))]

            for widget in square.winfo_children():
                widget.destroy()
        
            if not is_empty and piece and is_visible:
                label = tk.Label(square, text=piece, font=("Ariel", 24))
                label.pack()
    
    def update_board(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.get_piece(from_row, from_col)
        self.cursor.execute(
            "UPDATE chess SET `column` = %s, `row` = %s WHERE `row` = %s AND `column` = %s",
            (chr(to_col + ord('A')), to_row + 1, from_row + 1, chr(from_col + ord('A')))
        )
        self.cursor.execute(
            "UPDATE chess SET piece = NULL, `empty` = TRUE WHERE `row` = %s AND `column` = %s",
            (from_row+1, chr(from_col+ord('A')))
        )

        self.connection.commit()

        self.load_board_state()

    def get_piece(self, row, col):
        self.cursor.execute(
            "SELECT piece FROM chess WHERE `row` = %s AND `column` = %s",
            (row+1, chr(col+ord('A')))
        )
        return self.cursor.fetchone()[0]
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()

chessboard = Chessboard(db_config)
chessboard.protocol("WM_DELETE_WINDOW", chessboard.close_connection)
chessboard.mainloop