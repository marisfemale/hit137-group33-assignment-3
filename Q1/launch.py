# launch.py
import tkinter as tk
from GUI import MiniPhotoshopApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPhotoshopApp(root)
    root.mainloop()
