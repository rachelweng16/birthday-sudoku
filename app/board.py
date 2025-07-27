import customtkinter as ctk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sudoku import SudokuBoard
from utils import resource_path
from theme import THEME
from PIL import Image
from customtkinter import CTkImage
from cake import Cake
from tkinter import Canvas, Tk, NW
from PIL import ImageTk
#for better styling/transparency
import pywinstyles

#TODO: changes wrong popup to disabled button for rounded corners
#TODO: move build bday buttons to helper
class Board:
    def __init__(self, root, theme, canvas, on_complete):
        # super().__init__(parent)
        self.root = root 
        #configure theme
        self.theme_mode = theme
        self.colors = THEME[self.theme_mode]

        #generating solution board and puzzle board:
        self.board = SudokuBoard()
        self.puzzle = self.board.generate()
        self.on_complete = on_complete

        # #canvas for layering
        self.canvas = canvas
        # self.canvas.place(x=0, y=0)

        #grid layout build
        self.grid_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.colors["opacity"])
        self.grid_frame.pack(pady=(15,15))
        pywinstyles.set_opacity(self.grid_frame, color=self.colors["opacity"])
        self.entries = []
        self.build_grid()

        #button options for letter selection/clear
        str = list("BIRTHDAY!")
        self.button_frame = ctk.CTkFrame(self.root, fg_color=self.colors["opacity"])
        pywinstyles.set_opacity(self.button_frame, color=self.colors["opacity"])
        self.button_frame.pack(pady=15)

        for char in str:
            btn = ctk.CTkButton(
                self.button_frame,
                text=char,
                text_color=self.colors["button_text"],
                fg_color=self.colors["birthday!_button"],
                bg_color=self.colors["opacity"],
                border_color=self.colors["entry_border"],
                border_width=2,
                font=("Courier", 18, "bold"),
                width=40,
                command=lambda l=char: self.fill_selected(l)
            )
            btn.pack(side="left", padx=1)
            # pywinstyles.set_opacity(btn, color=self.colors["opacity"])

        self.clear_btn = ctk.CTkButton(self.button_frame, text="Clear", 
            text_color=self.colors["button_text"],
            fg_color=self.colors["clear"], 
            border_color=self.colors["entry_border"],
            border_width=2,
            command=self.clear_selected,
            font=("Arial", 16),
            bg_color="transparent")
        self.clear_btn.pack(side="left")

        #check solution button
        self.check_button = ctk.CTkButton(self.root, text="Check", command=self.check_solution, font=("Arial", 16, "bold"), 
            fg_color="#74adf8",
            border_color=self.colors["entry_border"],
            border_width=2,
            bg_color=self.colors["opacity"])
        self.check_button.pack(pady=(10, 0))
        pywinstyles.set_opacity(self.check_button , color=self.colors["opacity"])

        #keep track of board:
        self.curr_board = [[self.entries[r][c].get().upper() for c in range(9)] for r in range(9)]
        self.selected_cell = None # keep track of r and c of selected cell

        # #place cake:
        self.cake = Cake()
        cake_img_path = resource_path(self.cake.get_cake())
        self.cake_img = Image.open(cake_img_path).resize((500,500))
        self.cake_img_tk = ImageTk.PhotoImage(self.cake_img)
        self.cake_canvas_id = self.canvas.create_image(960, 800, anchor="center", image=self.cake_img_tk)

        #create and hide popups:
        self.create_wrong_solution_popup()
        self.hide_wrong_solution_popup()

        #TEMP BUTTON
        # self.temp_button = ctk.CTkButton(self.root, text="clickme", command=self.clear_all, font=("Arial", 16, "bold"),
        #     fg_color="#74adf8",
        #     border_color=self.colors["entry_border"],
        #     border_width=2,
        #     bg_color=self.colors["opacity"])
        # self.temp_button.pack(pady=(10,0))

    def build_grid(self):
        self.entries = [] 
        #creating 2d list of entries - one for each cell on sudoku board
        for r in range(9):
            row = []
            for c in range(9):
                top_pad = 6 if r % 3 == 0 and r != 0 else 0
                left_pad = 6 if c % 3 == 0 and c != 0 else 0

                container = ctk.CTkFrame(
                    self.grid_frame,
                    width=42,
                    height=42,
                    fg_color="transparent",
                )
                container.grid(row=r, column=c, padx=(left_pad, 0), pady=(top_pad, 0))

                e = ctk.CTkEntry(
                    master=container,
                    width=45,
                    height=45,
                    font=("Courier", 18, "bold"),
                    justify="center",
                    fg_color=self.colors["entry_bg"],
                    border_color=self.colors["entry_border"]
                )
                e.configure(insertontime=0)

                e.bind("<Key>", lambda event: "break")
                e.bind("<Button-1>", lambda event, row=r, col=c: self.on_click_cell(row, col))
                e.pack()

                char = self.puzzle[r][c]
                #place starter non-empty cells - disable interaction for each
                if char != "":
                    e.insert(0, char)
                    e.configure(fg_color=self.colors["entry_disabled"], state="disabled")

                row.append(e)
            self.entries.append(row)

    def on_click_cell(self, r, c):
        #unhighlight prev selected cell
        if self.selected_cell:
            prev_r, prev_c = self.selected_cell
            self.entries[prev_r][prev_c].configure(border_color=self.colors["entry_border"])  #reset to default state

        #highlight new selected cell
        self.selected_cell = (r, c)
        self.entries[r][c].configure(border_color=self.colors["entry_border_select"], border_width=2) 

    def check_solution(self):
        # onclick -> collect into 2d list and pass to valid_board for solution checking
        valid = self.board.valid_board(self.curr_board)
        if not valid:
            self.show_wrong_solution_popup()
        else:
            self.clear_all()
            if self.on_complete:
                self.on_complete(self.cake_canvas_id)

    ##setup wrong solution popup
    def create_wrong_solution_popup(self):        
        self.wrong_popup = ctk.CTkLabel(
            self.root,
            text="",  # leave empty, we'll add widgets manually
            # corner_radius=20,
            fg_color=self.colors["wrong_popup"],
            width=600,
            height=150
        )
        self.wrong_popup.pack_propagate(False)
        label = ctk.CTkLabel(self.wrong_popup, text="At least one square is wrong or empty :( try again!", 
                             font=("Arial", 20, "bold"))
        label.pack(padx=10, pady=20)

        close_btn = ctk.CTkButton(self.wrong_popup, text="Close", command=self.hide_wrong_solution_popup,
            font=("Arial", 16, "bold"), fg_color="#74adf8", bg_color=self.colors["opacity"])
        close_btn.pack(pady=10)
        pywinstyles.set_opacity(close_btn, color=self.colors["opacity"])

    def show_wrong_solution_popup(self):
        if not self.wrong_popup_visible:
            self.wrong_popup.place(relx=0.5, rely=0.5, anchor="center")
            self.wrong_popup_visible = True
    def hide_wrong_solution_popup(self):
        self.wrong_popup.place_forget()
        self.wrong_popup_visible = False

    def fill_selected(self, char):
        #update board external and internally
        if self.selected_cell:
            r,c = self.selected_cell
            self.entries[r][c].delete(0, "end")
            self.curr_board[r][c] = ""
            
            if not self.board.is_valid(self.curr_board, r, c, char):
                self.entries[r][c].insert(0, char)
                self.entries[r][c].configure(fg_color=self.colors["entry_incorrect_bg"])
                self.cake.lose_candle()
                self.replace_cake()
            else:
                self.entries[r][c].insert(0, char)
                self.entries[r][c].configure(fg_color=self.colors["entry_bg"])

            self.curr_board[r][c] = char

    def clear_selected(self):
        #update board external and internally
        if self.selected_cell:
            r,c = self.selected_cell
            self.entries[r][c].delete(0, "end")
            if self.entries[r][c].cget("state") != "disabled":
                self.entries[r][c].configure(fg_color=self.colors["entry_bg"])
                self.curr_board[r][c] = ""
    
    def replace_cake(self):
        new_cake_path = resource_path(self.cake.get_cake())
        new_cake = Image.open(new_cake_path).resize((500,500))
        new_cake = ImageTk.PhotoImage(new_cake)
        self.cake_img_tk = new_cake
        self.canvas.itemconfig(self.cake_canvas_id, image=new_cake)

    #clear all elements of board (when board is completed)
    def clear_all(self):
        self.grid_frame.pack_forget()
        self.button_frame.pack_forget()
        self.check_button.pack_forget()
        # self.temp_button.pack_forget()
        self.canvas.itemconfigure(self.cake_canvas_id, state="hidden")
        self.canvas.after(2000, lambda: self.on_complete(self.cake_canvas_id))
