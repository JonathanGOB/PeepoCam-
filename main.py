from tkinter import Tk, Label, PhotoImage, Canvas
from tkinter.constants import CENTER
from PIL import Image
from PIL import ImageTk
from threading import Thread
import pyautogui
import time
from pynput.keyboard import Key, Listener, Controller

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
        self.canvas.create_image(self.background.width()/2 - 40, self.background.height()/2 - 32, anchor=CENTER, image=self.peepo)
        self.canvas.create_image(self.background.width() - 550, self.background.height() - 180, anchor=CENTER, image=self.keyboard)
        self.armLeftMove = self.canvas.create_image(375, 600, anchor=CENTER, image=self.armLeft)

        listener = Listener(on_press=self.keyboard_press, on_release=self.keyboard_up,suppress=True)
        listener.start()

        thread = Thread(target = self.move_mousearm)
        thread.setDaemon(True)
        thread.start()
    
    def move_mousearm(self):
        quadrants = [False, False, False, False]
        while True:
            width, height = 450, 450
            x, y = ((self.background.width() - 220) - width/2), ((self.background.height() - 220) - height/2)
            screenwidth, screenheight = 1920, 1080
            xmouse, ymouse = pyautogui.position()
            if (xmouse > screenwidth/2 and ymouse > screenheight/2 and quadrants[0] != True):
                self.canvas.move(self.mouseMove, -30, -30)
                self.canvas.move(self.armRightMove, -30, -30)
                self.reset(quadrants)
                quadrants[0] = True
            if (xmouse > screenwidth/2 and ymouse < screenheight/2 and quadrants[1] != True):
                self.canvas.move(self.mouseMove, -30, 30)
                self.canvas.move(self.armRightMove, -30, 30)
                self.reset(quadrants)
                quadrants[1] = True
            if (xmouse < screenwidth/2 and ymouse > screenheight/2 and quadrants[2] != True):
                self.canvas.move(self.mouseMove, 30, -30)
                self.canvas.move(self.armRightMove, 30, -30)
                self.reset(quadrants)
                quadrants[2] = True
            if (xmouse < screenwidth/2 and ymouse < screenheight/2 and quadrants[3] != True):
                self.canvas.move(self.mouseMove, 30, 30)
                self.canvas.move(self.armRightMove, 30, 30)   
                self.reset(quadrants)
                quadrants[3] = True

            time.sleep(0.1)
    
    def reset(self, quadrants):
        if(quadrants[0] == True):
            self.canvas.move(self.mouseMove, 30, 30)
            self.canvas.move(self.armRightMove, 30, 30)
            quadrants[0] = False
        if(quadrants[1] == True):
            self.canvas.move(self.mouseMove, 30, -30)
            self.canvas.move(self.armRightMove, 30, -30)
            quadrants[1] = False
        if(quadrants[2] == True):
            self.canvas.move(self.mouseMove, -30, 30)
            self.canvas.move(self.armRightMove, -30, 30)
            quadrants[2] = False
        if(quadrants[3] == True):
            self.canvas.move(self.mouseMove, -30, -30)
            self.canvas.move(self.armRightMove, -30, -30)
            quadrants[3] = False


    def create_resized_image(self, filename, width, height, angle=0):
        img = Image.open(filename)
        img = img.resize((width,height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img.rotate(angle))

    def keyboard_press(self, event):

        if not self.keysPressed:
            self.keysPressed = event
            self.canvas.move(self.armLeftMove, 10, 20)

    def keyboard_up(self, event):

        if self.keysPressed:
            self.canvas.move(self.armLeftMove, -10, -20)

        self.keysPressed = None

root = Tk()
peepoGui = PeepoCam(root)
root.mainloop()