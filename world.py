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

There are a few things the World must know in order to execute actions at a given step.
1. Facts about the board
    a. Dimensions of the board
    b. Locations of barriers
2. Facts about the players
    a. Locations of players
    b. Actions submitted by players
3. logic
    a.

Rendering graphics is completely incidental. This is especially clear in the AI vs AI case.

Which classes are active and which are passive? Which classes invoke methods?

'''
from collections import defaultdict
from player import Player

class World():
    def __init__(self, board_dim):
        self.commands = list()
        self.users = dict()
        self.players = dict()
        self.x_len = board_dim[0]
        self.y_len = board_dim[1]
        self.tiles = [['' for i in range(self.y_len)] for j in range(self.x_len)]
        self.game_over = False
        self.outcome = 0
        self.round = 0

    def add_user(self, user):
        id_ = user.id
        self.users[id_] = user
        player = Player(self, id_)
        user.player = player
        self.players[id_] = player
        if id_ == 1:
            player.x = 0
            player.y = 0
            self.tiles[0][0] = str(id_)
        if id_ == 2:
            player.x = self.x_len - 1
            player.y = self.y_len - 1
            self.tiles[self.x_len - 1][self.y_len - 1] = str(id_)

    def print_tiles(self):
        print '   |' + ' | '.join(['%02d'%i for i in range(self.y_len)]) +'|'
        i = 0
        for tile in self.tiles:
            temp = list()
            for t in tile:
                if not t:
                    temp.append('_')
                else:
                    temp.append(t)
            print i, temp, i
            i += 1
        print '   |' + ' | '.join(['%02d'%i for i in range(self.y_len)]) +'|'

    def receive_commands(self, commands):
        self._validate_commands(commands)
        self.commands += commands

    def clear_commands(self, id):
        self.commands = [c for c in self.commands if c.player.id != id]

    def _validate_commands(self, commands):
        pass

    def execute_logic(self):
        self.commands.sort()
        for command in self.commands:
            command.execute()
        #self.render(self.commands)
        self.commands = list()

    def check_victory(self):
        dead_players = list()
        for i in self.players:
            player = self.players[i]
            if player.health <= 0:
                dead_players.append(player.id)
        if len(dead_players) == 2:
            self.end_game(3)
        elif len(dead_players) == 1:
            self.end_game(dead_players[0])

    def end_game(self, id):
        self.game_over = True
        self.outcome = id
        if id == 3:
            print "Both players have died. Game is a tie!"
        elif id == 1:
            print "Player 1 has died. Player 2 wins!"
        elif id == 2:
            print "Player 2 has died. Player 1 wins!"
        else:
            self.game_over = False
            self.outcome = 0

    def run(self):
        self.print_tiles()
        while True:
            self.round += 1
            print "USER 1 COMMANDS"
            self.users[1].get_commands()
            print "USER 2 COMMANDS"
            self.users[2].get_commands()
            self.execute_logic()
            self.check_victory()
            print self.get_state()
            self.print_tiles()
            if self.game_over:
                break
            if self.round > 25:
                break


    def get_state(self):
        p1 = self.players[1]
        p2 = self.players[2]
        output = {
            'p1_x': p1.x,
            'p1_y': p1.y,
            'p2_x': p2.x,
            'p2_y': p2.y,
            'p1_health': p1.health,
            'p2_health': p2.health,
            'outcome': self.outcome
            }
        return output



    def check_tile(self, x, y):
        #returns item at location x, y. If out of bounds, return "NA"
        if min([x,y]) < 0:
            return "NA"
        try:
            return self.tiles[x][y]
        except IndexError:
            return "NA"
