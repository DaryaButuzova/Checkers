import tkinter as tk
from Checkers import CheckersBoard
from auth import create_window


if __name__ == "__main__":
    if create_window():
        root = tk.Tk()
        checkers_board = CheckersBoard(root)
        checkers_board.start_game()
        root.mainloop()
