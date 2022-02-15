from tkinter import Tk, Label, PhotoImage, Canvas
from tkinter.constants import CENTER
from PIL import Image
from PIL import ImageTk, ImageOps
from threading import Thread
import pyautogui
import time
from pynput.keyboard import Key, Listener, Controller
from PIL import GifImagePlugin
import copy

class PeepoCam:

    keysPressed = None

    def __init__(self, master):

        #setup master/root
        self.master = master
        master.title("PeepoCam!")
        
        #init images
        self.armLeft = PhotoImage(file="peepo\\arms_rm.png")
        self.keyboard = self.create_resized_image("peepo\\keyboard.png", 800, 800)
        self.mousepad = self.create_resized_image("peepo\\mousemat_rm.png", 450, 450, angle=10)
        self.mouse = self.create_resized_image("peepo\\mouse.png", PhotoImage(file="peepo\\mouse.png").width(), PhotoImage(file="peepo\\mouse.png").height(), 300, mirror=True)
        self.armRight = PhotoImage(file="peepo\\arms_rm.png")
        self.peepo = PhotoImage(file="peepo\\peepo_half_white_removed.png")
        self.table = PhotoImage(file="peepo\\table.png")
        self.background = PhotoImage(file="peepo\\bg.png")
        self.frames, self.n_frames = self.get_frames("peepo\\giphy.gif", self.background.width(), self.background.height())
        self.canvas = Canvas(master, width = self.background.width(), height = self.background.height())  
        self.canvas.pack()

        # setup in canvas
        self.backgroundMove = self.canvas.create_image(self.background.width()/2, self.background.height()/2 - 200, anchor=CENTER, image=self.frames[0])
        self.canvas.create_image(self.background.width()/2, self.background.height()/2, anchor=CENTER, image=self.table)
        self.canvas.create_image(self.background.width() - 220, self.background.height() - 220, anchor=CENTER, image=self.mousepad)
        self.mouseMove = self.canvas.create_image(self.background.width() - 220, self.background.height() - 240, anchor=CENTER, image=self.mouse)
        self.armRightMove = self.canvas.create_image(650, 550, anchor=CENTER, image=self.armRight)
        self.canvas.create_image(self.background.width()/2 - 40, self.background.height()/2 - 32, anchor=CENTER, image=self.peepo)
        self.canvas.create_image(self.background.width() - 550, self.background.height() - 180, anchor=CENTER, image=self.keyboard)
        self.armLeftMove = self.canvas.create_image(375, 600, anchor=CENTER, image=self.armLeft)

        #setup keyboard listener
        listener = Listener(on_press=self.keyboard_press, on_release=self.keyboard_up)
        listener.start()

        thread_gif = Thread(target = self.update_frame)
        thread_gif.setDaemon(True)
        thread_gif.start()

        #setup mouse 
        thread = Thread(target = self.move_mousearm)
        thread.setDaemon(True)
        thread.start()


    def get_frames(self, gif, width, height):
        size = width, height
        imageObject = Image.open(gif)
        frames = []
        for frame in range(0,imageObject.n_frames):
            imageObject.seek(frame)
            img = copy.deepcopy(imageObject)
            img = img.resize(size, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img) # convert to PhotoImage
            frames.append(img)
        return frames, imageObject.n_frames
    
    def update_frame(self, fps = 10):
        ind = 0
        while True:
            time.sleep(0.1)
            frame = self.frames[ind]
            ind += 1
            if ind == self.n_frames:
                ind = 0
            self.canvas.itemconfig(self.backgroundMove, image = frame)


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


    def create_resized_image(self, filename, width, height, angle=0, mirror=False):
        img = Image.open(filename)
        if mirror:
            img = ImageOps.mirror(img)
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