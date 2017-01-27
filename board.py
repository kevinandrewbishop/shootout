'''
Note: at this point I need to decide if the "Board" and the "World" are the same

Overall basic game loop is as follows:
    1) AI/Humans evaluate situation and submit (valid) actions to World.
    2) World sorts submitted actions in the following order:
        a) Action number (1-3)
        b) Action type (rest, shield, move, shoot)
        c) Player number (1, 2) #Player number is irrelevant, just breaks tie
    3) For each action number, World executes then renders on the Board.

Because AI is such a big deal, I want to completely decouple AI from the raw
game mechanics. Ideally the game would be able to run the same way regardless
of whether it's human v human, human v AI, or AI v AI. There should be some sort
of API for the AI.

It's probably best to start with human v human only to get the mechanics down.
Once this is finished, begin work on the AI and its API.

HTTP API?
http://stackoverflow.com/questions/16213235/communication-between-two-python-scripts


This implies a few things:
1. The World must be able to take in each user's actions.
2. The World must execute the logic of those actions.
3. The World must give feedback to the users regarding what the outcome of the logic is.

Rendering graphics is completely incidental. This is especially clear in the AI vs AI case.

'''
import random
from random import randint
from pprint import pprint

class Board():
    def __init__(self, dimx = 15, dimy = 20):
        self.dimx = dimx
        self.dimy = dimy
        self._initialize(6)
        self.players = list()

    def _initialize2(self, num_barriers):
        self.board = [['_']*self.dimx for i in range(self.dimy)]
        for i in range(num_barriers):
            board_len = randint(4, 9)
            x = randint(1, self.dimx - 2)
            y = randint(1, self.dimy - 2)
            print x, y
            self.board[y][x] = 'X'
            for j in range(board_len):
                while True:
                    x_ = x + randint(-1, 1)
                    y_ = y + randint(-1, 1)
                    if x_ > 1 and x_ < self.dimx:
                        if y_ > 1 and y_ < self.dimy:
                            break
                x = x_
                y = y_
                print x, y
                self.board[y][x] = 'X'

    def _initialize(self, num_barriers):
        self.board = [['_']*self.dimx for i in range(self.dimy)]
        barriers = [[i, j] for j in [0.25, 0.75] for i in [0.25, 0.75]]
        for b in barriers:
            x = int(b[0]*self.dimx)
            y = int(b[1]*self.dimy)
            self.board[y][x] = 'X'
            for j in range(6):
                while True:
                    x_ = x + randint(-1, 1)
                    y_ = y + randint(-1, 1)
                    if x_ > 1 and x_ < self.dimx:
                        if y_ > 1 and y_ < self.dimy:
                            break
                x = x_
                y = y_
                self.board[y][x] = 'X'



    def __repr__(self):
        out = '    ' + '   '.join(['%02d' %i for i in range(self.dimx)]) +'\n'
        for i, row in enumerate(self.board):
            out += '%02d' %i
            out += str(row)
            out += '%02d' %i
            out += '\n'
        out += '    ' + '   '.join(['%02d' %i for i in range(self.dimx)])
        return out

    def add_player(self, player):
        self.players.append(player)

if __name__ == '__main__':
    board = Board()
    print board
    for i in range(3):
        print board
