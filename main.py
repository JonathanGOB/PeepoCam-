from tkinter import Tk, Label, PhotoImage, Canvas
from tkinter.constants import CENTER

class PeepoCam:

    keysPressed = None

    def __init__(self, master):
        self.master = master
        master.title("PeepoCam!")

        self.armLeft = PhotoImage(file="peepo\\arms_rm.png")
        self.keyboard = PhotoImage(file="peepo\\keyboard.png")
        self.armRight = PhotoImage(file="peepo\\arms_rm.png")
        self.peepo = PhotoImage(file="peepo\\peepo_half_white_removed.png")
        self.table = PhotoImage(file="peepo\\table.png")
        self.background = PhotoImage(file="peepo\\bg.png")
        
        self.canvas = Canvas(master, width = self.background.width(), height = self.background.height())  
        self.canvas.pack()

        self.canvas.create_image(self.background.width()/2, self.background.height()/2, anchor=CENTER, image=self.background)
        self.canvas.create_image(self.background.width()/2, self.background.height()/2, anchor=CENTER, image=self.table)
        self.armRightMove = self.canvas.create_image(650, 550, anchor=CENTER, image=self.armRight)
        self.canvas.create_image(self.background.width()/2 - 40, self.background.height()/2 - 33, anchor=CENTER, image=self.peepo)
        self.canvas.create_image(self.background.width() - 500, self.background.height() - 200, anchor=CENTER, image=self.keyboard)
        self.armLeftMove = self.canvas.create_image(375, 600, anchor=CENTER, image=self.armLeft)
        master.bind("<KeyPress>", self.keyboard_press)
        master.bind("<KeyRelease>", self.keyboard_up)
        
    def keyboard_press(self, event):
        print(self.keysPressed)

        if not self.keysPressed:
            self.keysPressed = event.char
            self.canvas.move(self.armLeftMove, 10, 20)

    def keyboard_up(self, event):
        print(self.keysPressed)

        if self.keysPressed:
            self.canvas.move(self.armLeftMove, -10, -20)

        self.keysPressed = None

root = Tk()
peepoGui = PeepoCam(root)
root.mainloop()