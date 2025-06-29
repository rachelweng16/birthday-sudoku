import customtkinter as ctk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.sudoku import SudokuBoard
from theme import THEME
from PIL import Image
from customtkinter import CTkImage
from cake import Cake
from tkinter import Canvas, Tk, NW
from PIL import ImageTk
#for better styling/transparency
import pywinstyles

#TODO: configure on run -> menu app -> launch board/gameplay logic/struct
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #configure theme
        self.theme_mode = "dark"
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
        bg_img = Image.open(self.colors["backdrop"])
        self.bg_img_tk = ImageTk.PhotoImage(bg_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img_tk)

        #board title
        self.label = ctk.CTkLabel(self, text = "🎉 Birthday! Sudoku 🎉", 
                                  font=("Arial", 42, "bold"), 
                                  bg_color=self.colors["opacity"])
        self.label.pack(pady=(55,10))
        pywinstyles.set_opacity(self.label, color=self.colors["opacity"])

        #grid layout build
        self.grid_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.colors["opacity"])
        self.grid_frame.pack(pady=(15,15))
        pywinstyles.set_opacity(self.grid_frame, color=self.colors["opacity"])
        self.entries = []
        self.build_grid()

        #button options for letter selection/clear
        str = list("BIRTHDAY!")
        button_frame = ctk.CTkFrame(self, fg_color=self.colors["opacity"])
        pywinstyles.set_opacity(button_frame, color=self.colors["opacity"])
        button_frame.pack(pady=15)

        for char in str:
            btn = ctk.CTkButton(
                button_frame,
                text=char,
                text_color=self.colors["button_text"],
                fg_color=self.colors["birthday!_button"],
                bg_color=self.colors["opacity"],
                font=("Courier", 18, "bold"),
                width=40,
                command=lambda l=char: self.fill_selected(l)
            )
            btn.pack(side="left", padx=1)
            # pywinstyles.set_opacity(btn, color=self.colors["opacity"])

        clear_btn = ctk.CTkButton(button_frame, text="Clear", 
                                  text_color=self.colors["button_text"],
                                  fg_color=self.colors["clear"], 
                                  command=self.clear_selected,
                                  font=("Arial", 16),
                                  bg_color="transparent")
        clear_btn.pack(side="left")

        #check solution button
        self.check_button = ctk.CTkButton(self, text="Check", command=self.check_solution, font=("Arial", 16, "bold"), 
                                          fg_color="#74adf8",
                                          bg_color=self.colors["opacity"])
        self.check_button.pack(pady=(10, 0))
        pywinstyles.set_opacity(self.check_button , color=self.colors["opacity"])

        #keep track of board:
        self.curr_board = [[self.entries[r][c].get().upper() for c in range(9)] for r in range(9)]
        self.selected_cell = None # keep track of r and c of selected cell

        # #place cake:
        self.cake = Cake()
        cake_img = Image.open(self.cake.get_cake()).resize((500,500))
        self.cake_img_tk = ImageTk.PhotoImage(cake_img)
        self.canvas.create_image(960, 800, anchor="center", image=self.cake_img_tk)

        #create and hide popups:
        self.create_wrong_solution_popup()
        self.hide_wrong_solution_popup()

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

        # self.entries[r][c].configure(border_color = "#565B5E")
        # self.selected_entry = box
        # box.configure(border_width=2, border_color = "#A7C7E7")

    def check_solution(self):
        # onclick -> collect into 2d list and pass to valid_board for solution checking
        valid = self.board.valid_board(self.curr_board)
        if not valid:
            self.show_wrong_solution_popup()
        #else:
        print(valid)

    ##setup wrong solution popup
    def create_wrong_solution_popup(self):        
        self.wrong_popup = ctk.CTkLabel(
            self,
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

if __name__ == "__main__":
    app = App()
    ctk.set_appearance_mode(app.theme_mode)
    ctk.set_default_color_theme("blue")
    #run app
    app.mainloop()  
