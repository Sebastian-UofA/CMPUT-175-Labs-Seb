#----------------------------------------------------
# Lab 3: Numerical Tic Tac Toe class
# 
# Author: 
# Collaborators:
# References:
#----------------------------------------------------

class NumTicTacToe:
    def __init__(self):
        '''
        Initializes an empty Numerical Tic Tac Toe board.
        Inputs: none
        Returns: None
        '''       
        self.board = [] # list of lists, where each internal list represents a row
        self.size = 3   # number of columns and rows of board
        
        # populate the empty squares in board with 0
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.board.append(row)
                
                
    def drawBoard(self):
        '''
        Displays the current state of the board, formatted with column and row 
        indicies shown.
        Inputs: none
        Returns: None
        '''
        # TO DO: delete pass and print out formatted board
        # e.g. an empty board should look like this:
        #    0   1   2  
        # 0    |   |   
        #   -----------
        # 1    |   |   
        #   -----------
        # 2    |   |           
        
        print("\n   0   1   2")
        for i in range(3):
            print(i, end=" ")
            for j in range(3):
                if self.board[i][j] != 0:
                    print(" ", self.board[i][j], end=" ")
                else:
                    print("   ", end="")
                if j != 2:
                    print("|", end="")
            print()
            if i != 2:
                print("  -----------")

    def squareIsEmpty(self, row, col):
        '''
        Checks if a given square is empty, or if it already contains a number 
        greater than 0.
        Inputs:
           row (int) - row index of square to check
           col (int) - column index of square to check
        Returns: True if square is empty; False otherwise
        '''
        # TO DO: delete pass and complete method
        return self.board[row][col] == 0
    
    
    def update(self, row, col, num):
        '''
        Assigns the integer, num, to the board at the provided row and column, 
        but only if that square is empty.
        Inputs:
           row (int) - row index of square to update
           col (int) - column index of square to update
           num (int) - entry to place in square
        Returns: True if attempted update was successful; False otherwise
        '''
        # TO DO: delete pass and complete method
        if self.squareIsEmpty(row, col):
            self.board[row][col] = num
            return True
        else:
            return False
    
    
    def boardFull(self):
        '''
        Checks if the board has any remaining empty squares.
        Inputs: none
        Returns: True if the board has no empty squares (full); False otherwise
        '''
        # TO DO: delete pass and complete method
        for i in range(self.size):
            for j in range(self.size):
                if self.squareIsEmpty(i, j):
                    return False
        return True
        
           
    def isWinner(self):
        '''
        Checks whether the current player has just made a winning move.  In order
        to win, the player must have just completed a line (of 3 squares) that 
        adds up to 15. That line can be horizontal, vertical, or diagonal.
        Inputs: none
        Returns: True if current player has won with their most recent move; 
                 False otherwise
        '''
        # TO DO: delete pass and complete method
        for i in range(3):
            if sum(self.board[i]) == 15 or sum(self.board[j][i] for j in range(3)) == 15:
                return True
        if self.board[0][0] + self.board[1][1] + self.board[2][2] == 15 or \
                self.board[0][2] + self.board[1][1] + self.board[2][0] == 15:
            return True
        return False
     

if __name__ == "__main__":
    # start by creating empty board and checking the contents of the board attribute
    myBoard = NumTicTacToe()
    print('Contents of board attribute when object first created:')
    print(myBoard.board)
    
    # does the empty board display properly?
    myBoard.drawBoard()

    # assign a number to an empty square and display
    print("\nTest update method:")
    print(myBoard.update(1, 1, 5))  # Should be True
    myBoard.drawBoard()

    # try to assign a number to a non-empty square. What happens?
    print(myBoard.update(1, 1, 3))  # Should be False, square already taken
    myBoard.drawBoard()

    # check if the board has a winner. Should there be a winner after only 1 entry?
    print("\nTest isWinner method:")
    print(myBoard.isWinner())  # Should be False

    # check if the board is full. Should it be full after only 1 entry?
    print("\nTest boardFull method:")
    print(myBoard.boardFull())  # Should be False

    # add values to the board so that any line adds up to 15. Display
    myBoard.update(0, 0, 5)
    myBoard.update(0, 1, 3)
    myBoard.update(0, 2, 7)
    myBoard.drawBoard()

    # check if the board has a winner
    print("\nTest isWinner method:")
    print(myBoard.isWinner())  # Should be True

    # check if the board is full
    print("\nTest boardFull method:")
    print(myBoard.boardFull())  # Should be False

    # write additional tests, as needed

    