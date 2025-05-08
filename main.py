import tkinter as tk
import configs as configs
print(dir(configs))
root = tk.Tk()

# Window format
root.title(configs.window_title)
root.geometry(configs.window_size)


#button open action
def button_open_clicked():
    print('hi')

#button open outlook
button_open = tk.Button(root, command=button_open_clicked, text=configs.button_open_text,**configs.button_open_style)


#run
button_open.pack()

root.mainloop()