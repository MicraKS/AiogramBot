from tkinter import *

root = Tk()
root.title("Программирование Python")

WIDTH = 640
HEIGHT = 480

def winfo_screen(one, two):
    x = root.winfo_screenwidth() // 2 - one // 2
    y = root.winfo_screenheight() // 2 - two // 2
    return x,y

# root.winfo_screenwidth() и root.winfo_screenheight() - вычислить размеры окна
POS_X, POS_Y = winfo_screen(WIDTH,HEIGHT)
# POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

# resizable - запрет на изменение окна в высоту и ширину
root.resizable(False,False)

xx, yy = winfo_screen(190, 100)
lable_one = Label(root, text="Привет, я Tkinter", font="Consolas 20")
lable_one.place[x] = xx
lable_one.place["y"] = yy

okButton = Button(root, text="OK", width="20", font="Consolas 10")
okButton.place(x=X, y=Y)

root.mainloop()