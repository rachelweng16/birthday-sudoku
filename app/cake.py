import customtkinter as ctk
import pywinstyles
from PIL import Image
from customtkinter import CTkImage

#cake obj
#diff graphics
#animation described when loosing candle
#animation of cake transformation based on # candles lost
#idea is that when you flag a wrong move, this changes graphics and handles that logic

class Cake():
    def __init__(self):
        self.candles = 9

    def lose_candle(self):
        self.candles -= 1

    def get_cake(self):
        return "img/cake_" + str(self.candles) + ".png"


# print(Image.open("img/cake_9.png").mode)