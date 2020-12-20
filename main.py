from tkinter import Tk, Label, PhotoImage, Canvas
from tkinter.constants import CENTER
from PIL import Image
from PIL import ImageTk
from ctypes import windll, Structure, c_long, byref
from threading import Thread
import pyautogui
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]



def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

class PeepoCam:

    keysPressed = None

    def __init__(self, master):
        self.master = master
        master.title("PeepoCam!")
        
        self.armLeft = PhotoImage(file="peepo\\arms_rm.png")
        self.keyboard = self.create_resized_image("peepo\\keyboard.png", 800, 800)
        self.mousepad = self.create_resized_image("peepo\\mousemat_rm.png", 450, 450, angle=10)
        self.mouse = self.create_resized_image("peepo\\mouse.png", PhotoImage(file="peepo\\mouse.png").width(), PhotoImage(file="peepo\\mouse.png").height(), 180)
        self.armRight = PhotoImage(file="peepo\\arms_rm.png")
        self.peepo = PhotoImage(file="peepo\\peepo_half_white_removed.png")
        self.table = PhotoImage(file="peepo\\table.png")
        self.background = PhotoImage(file="peepo\\bg.png")
        
        self.canvas = Canvas(master, width = self.background.width(), height = self.background.height())  
        self.canvas.pack()

        self.canvas.create_image(self.background.width()/2, self.background.height()/2, anchor=CENTER, image=self.background)
        self.canvas.create_image(self.background.width()/2, self.background.height()/2, anchor=CENTER, image=self.table)
        self.canvas.create_image(self.background.width() - 220, self.background.height() - 220, anchor=CENTER, image=self.mousepad)
        self.mouseMove = self.canvas.create_image(self.background.width() - 220, self.background.height() - 240, anchor=CENTER, image=self.mouse)
        self.armRightMove = self.canvas.create_image(650, 550, anchor=CENTER, image=self.armRight)
        self.canvas.create_image(self.background.width()/2 - 40, self.background.height()/2 - 33, anchor=CENTER, image=self.peepo)
        self.canvas.create_image(self.background.width() - 550, self.background.height() - 180, anchor=CENTER, image=self.keyboard)
        self.armLeftMove = self.canvas.create_image(375, 600, anchor=CENTER, image=self.armLeft)

        master.bind("<KeyPress>", self.keyboard_press)
        master.bind("<KeyRelease>", self.keyboard_up)
        thread = Thread(target = self.move_mousearm)
        thread.setDaemon(True)
        thread.start()
    
    def move_mousearm(self):
        while True:
            width, height = 450, 450
            x, y = ((self.background.width() - 220) - width/2), ((self.background.height() - 220) - height/2)
            screenwidth, screenheight = 1920, 1080
            xmouse, ymouse = pyautogui.position()
            translatedWidthSteps, translateHeightSteps = width/screenwidth, height/screenheight
            print(x + (xmouse*translatedWidthSteps), y + (ymouse*translateHeightSteps))
            self.canvas.move(self.mouseMove, x + (xmouse*translatedWidthSteps), y + (ymouse*translateHeightSteps))


    def create_resized_image(self, filename, width, height, angle=0):
        img = Image.open(filename)
        img = img.resize((width,height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img.rotate(angle))

    def keyboard_press(self, event):

        if not self.keysPressed:
            self.keysPressed = event.char
            self.canvas.move(self.armLeftMove, 10, 20)

    def keyboard_up(self, event):

        if self.keysPressed:
            self.canvas.move(self.armLeftMove, -10, -20)

        self.keysPressed = None

root = Tk()
peepoGui = PeepoCam(root)
root.mainloop()