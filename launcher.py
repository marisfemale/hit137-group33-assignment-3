import tkinter as tk
import subprocess
import sys
import configs

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title(configs.window_title)
        self.root.geometry(configs.window_geometry)
        
        frame = tk.Frame(root)
        frame.pack(expand=True)

        photo_btn = tk.Button(
            frame,
            text=configs.button_photo_text,
            width=configs.button_width,
            command=self.launch_photo_editor
        )
        photo_btn.pack(pady=configs.button_pad_y)

        game_btn = tk.Button(
            frame,
            text=configs.button_game_text,
            width=configs.button_width,
            command=self.launch_game
        )
        game_btn.pack(pady=configs.button_pad_y)

    def launch_photo_editor(self):
        subprocess.Popen([sys.executable, configs.photo_editor_script])

    def launch_game(self):
        subprocess.Popen([sys.executable, configs.game_script])

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()
