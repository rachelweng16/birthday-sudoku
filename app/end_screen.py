import customtkinter as ctk
import sys
import os
from theme import THEME
from PIL import Image
from customtkinter import CTkImage
from cake import Cake
from utils import resource_path
from tkinter import Canvas, Tk, NW
from PIL import ImageTk
#for better styling/transparency
import pywinstyles

class End:
    def __init__(self, root, canvas, cake_id):
        self.root=root
        #import cake
        self.canvas = canvas
        #on_call - cake should be hidden
        self.cake_canvas_id = cake_id

        #place cake plate
        plate_img_path = resource_path("img/plate.png")
        self.plate_img = Image.open(plate_img_path).resize((960,540))
        self.plate_img_tk = ImageTk.PhotoImage(self.plate_img)
        self.plate_canvas_id = self.canvas.create_image(960, 700, anchor="center", image=self.plate_img_tk)
        self.canvas.tag_raise(self.cake_canvas_id, self.plate_canvas_id)

        self.canvas.coords(self.cake_canvas_id, 960, 400)
        self.canvas.itemconfigure(self.cake_canvas_id, state="normal")

        #place bday sign and confetti
        bday_sign_path = resource_path("img/bday_sign.png")
        self.bday_sign = Image.open(bday_sign_path).resize((768,432))
        self.bday_sign_tk = ImageTk.PhotoImage(self.bday_sign)
        self.bday_sign_canvas_id = self.canvas.create_image(960, 200, anchor="center", image=self.bday_sign_tk)
        confetti_path = resource_path("img/confetti.png")
        self.confetti = Image.open(confetti_path).resize((1152, 480))
        self.confetti_tk = ImageTk.PhotoImage(self.confetti)
        self.confetti_canvas_id = self.canvas.create_image(960, 150, anchor="center", image=self.confetti_tk)

        #place flag and 
        flag_path = resource_path("img/flag.png")
        self.flag = Image.open(flag_path).resize((480,270))
        self.flag_tk = ImageTk.PhotoImage(self.flag)
        self.flag_canvas_id = self.canvas.create_image(1225, 755, anchor="center", image=self.flag_tk)
        balloon_path = resource_path("img/balloon.png")
        self.balloon = Image.open(balloon_path).resize((1920, 1080))
        self.balloon_tk = ImageTk.PhotoImage(self.balloon)
        self.balloon_canvas_id = self.canvas.create_image(320, 700, anchor="center", image=self.balloon_tk)


#USE AFTERs