import tkinter as tk
from tkinter import filedialog
import configs as configs
import cv2
import matplotlib.pyplot as plt


print(dir(configs))
root = tk.Tk()

# Window format
root.title(configs.window_title)
root.geometry(configs.window_size)


#button open action
def button_open_clicked():
    file_path = tk.filedialog.askopenfilename()
    #load image
    img=cv2.imread(file_path)
    #convert color form BGR to RGB
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #display img
    plt.imshow(img)
    plt.show()


#button open outlook
button_open = tk.Button(root, command=button_open_clicked, text=configs.button_open_text,**configs.button_open_style)


#run
button_open.pack()

root.mainloop()