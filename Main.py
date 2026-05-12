import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
from guı import SudokuGUI
from config import API_KEY

def main():
    
    
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()