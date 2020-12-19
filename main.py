from tkinter import Tk, Label, Button, Canvas, PhotoImage

class PeepoCam:
    def __init__(self, master):
        self.master = master
        master.title("PeepoCam!")

        self.image = PhotoImage(file="peepo\\base_shadow_bg.png")
        self.label = Label(master, image=self.image)
        self.label.pack()

root = Tk()
peepoGui = PeepoCam(root)
root.mainloop()