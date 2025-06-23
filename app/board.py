import customtkinter as ctk
from src.sudoku import SudokuBoard
from theme import THEME
from PIL import Image
from customtkinter import CTkImage
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

        #bg image:
        bg_img = CTkImage(Image.open(self.colors["backdrop"]), size=(1920,1080))
        label = ctk.CTkLabel(self, image=bg_img, text="")
        label.place(relx=0, rely=0, relwidth=1, relheight=1)

        #board title
        self.label = ctk.CTkLabel(self, text = "🎉 Birthday! Soduku 🎉", 
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
                width=40,
                command=lambda l=char: self.fill_selected(l)
            )
            btn.pack(side="left", padx=1)
            # pywinstyles.set_opacity(btn, color=self.colors["opacity"])

        clear_btn = ctk.CTkButton(button_frame, text="CLEAR", 
                                  text_color=self.colors["button_text"],
                                  fg_color=self.colors["clear"], 
                                  command=self.clear_selected,
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
        print(valid)


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
