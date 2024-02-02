class NumTicTacToe:
    def __init__(self):
        self.board = [[0]*3 for _ in range(3)]

    def squareIsEmpty(self, row, col):
        return self.board[row][col] == 0

    def update(self, row, col, num):
        if self.squareIsEmpty(row, col):
            self.board[row][col] = num
            return True
        return False

    def boardFull(self):
        return all(self.board[row][col] != 0 for row in range(3) for col in range(3))

    def isWinner(self):
        for i in range(3):
            if sum(self.board[i]) == 15 or sum(self.board[j][i] for j in range(3)) == 15:
                return True
        if sum(self.board[i][i] for i in range(3)) == 15 or sum(self.board[i][2-i] for i in range(3)) == 15:
            return True
        return False

# Testing
game = NumTicTacToe()

# Test squareIsEmpty method
print(game.squareIsEmpty(0, 0))  # Should print: True

# Test update method
print(game.update(0, 0, 1))  # Should print: True
print(game.squareIsEmpty(0, 0))  # Should print: False
print(game.update(0, 0, 2))  # Should print: False

# Test boardFull method
print(game.boardFull())  # Should print: False
for i in range(3):
    for j in range(3):
        game.update(i, j, 1)
print(game.boardFull())  # Should print: True

# Test isWinner method
game = NumTicTacToe()
game.update(0, 0, 5)
game.update(0, 1, 5)
game.update(0, 2, 5)
print(game.isWinner())  # Should print: True
