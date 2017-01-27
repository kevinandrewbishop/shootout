'''

'''
from config import NUM_ACTIONS, VALID_ACTIONS
from player import Player

class Command():
    def __init__(self, number, action, player, params = None):
        self.number = number
        self.action = action
        self.params = params
        self.player = player

        self.validate()
        self.rank = self.get_rank()

    def validate(self):
        if self.number not in list(range(NUM_ACTIONS)):
            msg = 'Number must be between 1 and %s got %s'
            raise ValueError(msg %(NUM_ACTIONS, self.number))

        if self.action not in VALID_ACTIONS:
            msg = 'Action must be rest, shield, move, shoot. Got %s'
            raise ValueError(msg %self.action)

        if self.action == 'move':
            if self.params not in ['u', 'l', 'd', 'r']:
                msg = 'When moving, params must be u, l, d, or r. Got %s'
                raise ValueError(msg %self.params)

        if self.action == 'shoot':
            if not isinstance(self.params, tuple):
                msg = 'When shooting, params must be tuple containing '
                msg += 'coordinates of target. Got %s'
                raise ValueError(msg %self.params)
            if not len(self.params) == 2:
                msg = 'When shooting, param tuple must be of length 2 containing'
                msg += ' x and y coordinates of target. Got %s'
                raise ValueError(msg %len(self.params))
            if not isinstance(self.params[0], int) and isinstance(self.params[1], int):
                msg = 'When shooting, param tuple elements but be of type int. Got %s, %s'
                raise ValueError(msg %(type(self.params[0]), type(self.params[1])))

        if not isinstance(self.player, Player):
            msg = 'player must be of type Player. Got %s'
            raise ValueError(msg %type(self.player))

    def get_rank(self):
        '''
        Actions are executed by the World in a certain order.
        Specifically, they are sorted by:
            a) Action number (1-3)
            b) Action type (rest, shield, move, shoot)
            c) Player number (1, 2) #Player number is irrelevant, just breaks tie
        This returns a rank so that actions may be sorted.
        '''
        action_ranks = {
            'rest': 0,
            'shield': 1,
            'move': 2,
            'shoot': 3
            }
        rank = self.number*100 + action_ranks[self.action]*10 + self.player.id
        return rank

    def __lt__(self, other):
        return self.rank < other.rank

    def execute(self):
        #print "I'm executing!"
        print "PLayer%s %s %s" %(self.player.id, self.action, self.params)
        action = getattr(self.player, self.action)
        action(self.params)

if __name__ == '__main__':
    class FakeBoard():
        def add_player(self, player):
            pass

    board = FakeBoard()
    player = Player(board)
    rest = Command(1, 'rest', player)
