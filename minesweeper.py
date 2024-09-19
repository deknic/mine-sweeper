import random
import re
import time

# create the board
class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create Board - using a helper function
        self.board = self.make_new_board()
        self.assign_values_to_board()
        # keep track of where the user has dug with a set
        self.dug = set()

    def make_new_board(self):
        # construct a new board based on the size of the board
        # and the numebr of bmbs that we pass in

        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] # creates a board:
        # [
        # [None, None...,None],
        # [None, None...,None],
        # [None, None...,None]
        #]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2-1)
            row = loc // self.dim_size
            col = row % self.dim_size
            if board[row][col] == '*': # there is a bomb already, continue
                continue
            
            board[row][col] = '*' # otherwise, plant the bomb
            bombs_planted += 1 # and icreament bombs planted

        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)
    
    def get_num_neighboring_bombs(self, row, col):
        num_neighbouring_bombs = 0
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

    def dig(self, row, col):
        # return True is successful False if there is a bomb
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self): # show board as a string to the user
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        # put board together as a string
        string_rep = ''
        # get max col widths for printing
        widths =[]
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(max(columns, key = len))
            )

        # print the CSV strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells =[]
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        string_rep += ' |'.join(cells)
        string_rep += ' |\n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += '\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# Play the game
def play(dim_size, num_bombs):
# 1. create the board, plant the bombs
    board = Board(dim_size, num_bombs)
# 2. show user board and ask where they want to dig 
# 3a. if location is a bomb, game over
# 3b. otherwise, dig recursively until each square is at least
#       next to a bomb state how many bombs are nearby
# 4. repeat 2 & 3 until there are no more places to dig
    safe = True
    while len(board.dug) < board.dim_size**2 - num_bombs:
        time.sleep(0.8)
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig; row, col? "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("invalid location.  Please try again")
            continue
        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("YOU HAVE WON!")
    else:
        print("GAME OVER!!!")
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play(10,6)