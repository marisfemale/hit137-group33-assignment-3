import tkinter as tk
import configs as configs
# print(dir(configs))
root = tk.Tk()

# Window format
root.title(configs.window_title)
root.geometry(configs.window_size)

#button open
tk.Button(configs.button_open)
root.mainloop()