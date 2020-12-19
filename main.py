from tkinter import Tk, Label, PhotoImage, Canvas
from tkinter.constants import CENTER

class PeepoCam:

    def __init__(self, master):
        self.master = master
        master.title("PeepoCam!")

        self.image = PhotoImage(file="peepo\\base_shadow_bg.png")
        self.canvas = Canvas(master, width = self.image.width(), height = self.image.height())  
        self.canvas.pack()

        self.canvas.create_image(self.image.width()/2, self.image.height()/2, anchor=CENTER, image=self.image)


root = Tk()
peepoGui = PeepoCam(root)
root.mainloop()