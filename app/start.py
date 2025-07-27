import customtkinter as ctk
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sudoku import SudokuBoard
from board import Board
from theme import THEME
from utils import resource_path
from PIL import Image
from customtkinter import CTkImage
from end_screen import End
from tkinter import Canvas, Tk, NW
from PIL import ImageTk
#for better styling/transparency
import pywinstyles

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #configure theme
        self.theme_mode = "light"
        self.colors = THEME[self.theme_mode]

        #generating solution board and puzzle board:
        self.board = SudokuBoard()
        self.puzzle = self.board.generate()

        #window size/title
        self.title("Birthday Sudoku")
        self.geometry("1920x1080")

        #canvas for layering
        self.canvas = Canvas(self, width=1920, height=1080, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        #bg image
        bg_img_path = resource_path(self.colors["backdrop"])
        bg_img = Image.open(bg_img_path)
        self.bg_img_tk = ImageTk.PhotoImage(bg_img)
        self.bg_img_id= self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img_tk)

        #board title
        self.label = ctk.CTkLabel(self, text = "🎉 Birthday! Sudoku 🎉", 
                                  font=("Arial", 42, "bold"), 
                                  bg_color=self.colors["opacity"])
        self.label.pack(pady=(55,10))
        pywinstyles.set_opacity(self.label, color=self.colors["opacity"])

        #making start button
        self.start_btn = ctk.CTkButton(self, text="Start", command=self.run_board, font=("Arial", 30, "bold"), 
            fg_color="#C899F8",
            border_color="#565B5E",
            border_width=2,
            bg_color=self.colors["opacity"])
        self.start_btn.pack(pady=(250, 0))
        pywinstyles.set_opacity(self.start_btn , color=self.colors["opacity"])

        #making dark/light mode toggle
        self.theme_toggle = ctk.CTkSegmentedButton(self, values=["Light Mode", "Dark Mode"],
            command=self.set_theme,
            unselected_color = "#99A7F8",
            unselected_hover_color = "#657AF0",
            selected_color = "#657AF0",
            selected_hover_color = "#657AF0",
            fg_color="#657AF0",
            bg_color=self.colors["opacity"])                                                 
        self.theme_toggle.pack(pady=(25, 350))
        self.theme_toggle.set("Light Mode")
        pywinstyles.set_opacity(self.theme_toggle, color=self.colors["opacity"])

    def run_board(self):
        self.theme_toggle.pack_forget()
        self.start_btn.pack_forget()
        self.board = Board(root=self, theme=self.theme_mode, canvas=self.canvas, on_complete=self.on_complete)

    def on_complete(self, cake_id):
        self.label.pack_forget()
        self.end = End(self, canvas=self.canvas, cake_id=cake_id)

    def set_theme(self, value): #live update of theme
        if value == "Light Mode":
            self.theme_mode = "light"
        elif value == "Dark Mode":
            self.theme_mode = "dark"
        ctk.set_appearance_mode(app.theme_mode) #change ctk appearance
        self.colors = THEME[self.theme_mode] #update self.colors
        dark_img_path = resource_path(self.colors["backdrop"])
        dark_img = Image.open(dark_img_path) #update backdrop
        self.bg_img_tk = ImageTk.PhotoImage(dark_img)
        self.canvas.itemconfig(self.bg_img_id, image=self.bg_img_tk)

if __name__ == "__main__":
    app = App()
    ctk.set_appearance_mode(app.theme_mode)
    ctk.set_default_color_theme("blue")
    #run app
    app.mainloop()  


