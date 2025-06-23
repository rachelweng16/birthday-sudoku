import random
import copy

class SudokuBoard:
    def __init__(self):
        self.LETTERS = list("BIRTHDAY!") # our 9 unique characters
        self.solution = None
        self.puzzle = None

    #builds unique soduku board, calls solve and remove cells to create puzzle
    #returns 2d list of partially solved puzzle
    def generate(self):
        board = [["" for i in range(9)] for j in range(9)]

        #creating a BIRTHDAY! string in order for a random row
        birthday_row = random.randint(0,8)
        #ensures ONE random row in the board will ALWAYS spell BIRTHDAY in order.
        for i in range(9):
            board[birthday_row][i] = self.LETTERS[i]
        
        #solving the board -> helper recursive fn using backtracking to fill board
        self.solve(board)
        self.solution = board

        #remove some cells to create puzzle
        self.puzzle = self.remove_cells(board)
        return self.puzzle

    #solve function- starts with randomly places letters across board - uses backtracking to create valid board from there
    #exits when board is solved and no empty cells remain.
    def solve(self, board):
        for row in range(9):
            for col in range(9):
                #case when empty cell found
                if board[row][col] == "":

                    #make trial iteration of letters random
                    letters_shuffled = self.LETTERS[:]
                    random.shuffle(letters_shuffled)

                    for char in letters_shuffled:
                        if self.is_valid(board, row, col, char):
                            board[row][col] = char
                            if self.solve(board):
                                return True
                            
                            board[row][col] = ""
                    
                    #if none of the chars we tried worked, backtrack
                    return False
        #we exit when board is solved and no empty cells exist
        return True

    #given current board state, the coordinates (row, col) and the char to be placed, return whether placing the char in (row, col) is valid.
    #a placement is valid if: the char is unique in its row, col, and 3x3 region.
    #precondition: the cell in (row, col) on board is empty.
    def is_valid(self, board, row, col, char):
        #1: char is unique in row and char is unique in col
        for i in range(9):
            if board[row][i] == char or board[i][col] == char:
                return False

        #2: char is unique in square zone
        zone_row = (row // 3) * 3
        zone_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if char == board[i + zone_row][j + zone_col]:
                    return False

        return True

    #remove cells to create easy-moderate level board
    #can ammend keep number to change difficulty.
    def remove_cells(self, board, keep = 37):
        board_rm = copy.deepcopy(board)

        #create a random list of cell positions to remove
        pos = []
        for r in range(9):
            for c in range(9):
                pos.append([r, c])
        random.shuffle(pos)

        count = 0
        for pair in pos:
            if count > keep:
                break
            board_rm[pair[0]][pair[1]] = ""
            count += 1

        return board_rm
    
    #called when user checks their answer, returns if board is valid
    #returns true if and only if every cell is valid on the board and no cell is empty. return false otherwise.
    #a placement is valid if: the char is unique in its row, col, and 3x3 region.
    def valid_board(self, board):
        for i in range(9):
            row = set()
            col = set()
            block = set()
            for j in range(9):
                #check rows [i][j]
                if board[i][j] in row or board[i][j] == "":
                    return False
                else:
                    row.add(board[i][j])
                
                #check columns in same pass [j][i]
                if board[j][i] in col:
                    return False
                else:
                    col.add(board[j][i])

                #check 3x3 region (9 regions total)
                r = 3 * (i // 3) + (j // 3)
                c = 3 * (i % 3) + (j % 3)
                if board[r][c] in block:
                    return False
                if board[r][c] != "":
                    block.add(board[r][c])
        return True


                



# # test board generation!
# puzzle_board = generate_board()
# print(remove_cells(puzzle_board))
    

