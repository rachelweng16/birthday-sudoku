import customtkinter as ctk
from src.sudoku import SudokuBoard

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        #generating solution board and puzzle board:
        self.board = SudokuBoard()
        self.puzzle = self.board.generate()

        #window size/title
        self.title("Birthday Sudoku")
        self.geometry("1000x800")

        #board title
        self.label = ctk.CTkLabel(self, text = "🎉 Birthday! Soduku 🎉", font=("Arial", 42, "bold"))
        self.label.pack(pady=1, padx=10, fill="x", anchor="center") 
        self.label.configure(state="disabled")

        #grid layout build
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=20)
        self.entries = []
        self.build_grid()

        #button options for letter selection/clear
        str = list("BIRTHDAY!")
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        for char in str:
            btn = ctk.CTkButton(
                button_frame,
                text=char,
                fg_color="#7A5A99",
                width=40,
                command=lambda l=char: self.fill_selected(l)
            )
            btn.pack(side="left", padx=2)

        clear_btn = ctk.CTkButton(button_frame, text="CLEAR", fg_color="#4C3464", command=self.clear_selected)
        clear_btn.pack(side="left", padx=6)

        #check solution button
        self.check_button = ctk.CTkButton(self, text="Check", command=self.check_solution, font=("Arial", 16, "bold"))
        self.check_button.pack(pady=10)

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
                    width=40,
                    height=40,
                    font=("Courier", 18, "bold"),
                    justify="center"
                )
                e.configure(insertontime=0)

                e.bind("<Key>", lambda event: "break")
                e.bind("<Button-1>", lambda event, row=r, col=c: self.on_click_cell(row, col))
                e.pack()

                char = self.puzzle[r][c]
                #place starter non-empty cells - disable interaction for each
                if char != "":
                    e.insert(0, char)
                    e.configure(fg_color="#292929", state="disabled")

                row.append(e)
            self.entries.append(row)

    def on_click_cell(self, r, c):
            #unhighlight prev selected cell
            if self.selected_cell:
                prev_r, prev_c = self.selected_cell
                self.entries[prev_r][prev_c].configure(border_color="#565B5E", border_width=1)  #reset to default state

            #highlight new selected cell
            self.selected_cell = (r, c)
            self.entries[r][c].configure(border_color="#A7C7E7", border_width=2) 

        # self.entries[r][c].configure(border_color = "#565B5E")
        # self.selected_entry = box
        # box.configure(border_width=2, border_color = "#A7C7E7")

    def check_solution(self):
        # onclick -> collect into 2d list for solution checking
        print("Current board:")
        for row in self.curr_board:
            print(row) #future will return board and can iteratively call is_valid on each cell
    
    def fill_selected(self, char):
        #update board external and internally
        if self.selected_cell:
            r,c = self.selected_cell
            self.entries[r][c].delete(0, "end")
            self.entries[r][c].insert(0, char)
            
            if not self.board.is_valid(self.curr_board, r, c, char):
                self.entries[r][c].configure(fg_color="#A84E4E")
            else:
                self.entries[r][c].configure(fg_color="#343638")

            self.curr_board[r][c] = char

    def clear_selected(self):
        #update board external and internally
        if self.selected_cell:
            r,c = self.selected_cell
            self.entries[r][c].delete(0, "end")
            if self.entries[r][c].cget("state") != "disabled":
                self.entries[r][c].configure(fg_color="#343638")
                self.curr_board[r][c] = ""

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    #run app
    app = App()
    app.mainloop()  
