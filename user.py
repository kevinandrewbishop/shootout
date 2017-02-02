'''
The interface for sending and receiving information to the game.
How users (human or AI) interact with the game itself.
'''
from command import Command
from config import VALID_ACTIONS


class User():
    def __init__(self, world, id, params = None):
        self.world = world
        self.id = id
        self.world.add_user(self)
        if not params:
            self.params = {'health_diff': 1,
                'los_bonus': 1,
                'dist_div': 20.,
                'health_diff_aggress': 1,
                'win': 5,
                'lose': -5}
        else:
            self.params = params

    def command(self, action, number):
        if action not in VALID_ACTIONS:
            print 'Action must be either %s.' %' '.join(VALID_ACTIONS)
            print 'Got %s' %action
            return None
        if action == 'clear':
            response = raw_input('Are you sure you want to clear all commands? (y/n)')
            if response.lower() == 'y':
                self.world.clear_commands(self.id)
                return 'clear all'
            return 'cancel'
        if action == 'rest':
            print 'Resting'
        if action == 'shield':
            print 'Shield Up'
        if action == 'move':
            direction = ''
            while direction not in ['u', 'd', 'l', 'r']:
                direction = raw_input('Which direction? (u/d/l/r)')
            print 'Moving %s' %direction
            command = Command(number, action, self.player, direction)
            return command
        if action == 'shoot':
            coord = raw_input('Enter space delimited coordinates. (e.g. "5 12")')
            coord = tuple(coord.split(' '))
            coord = (int(coord[0]), int(coord[1]))
            print "shooting at %s, %s" %coord
            command = Command(number, action, self.player, coord)
            return command
        command = Command(number, action, self.player)
        return command

    def get_commands(self):
        num_actions = 3
        i = 0
        commands = list()
        while i < num_actions:
            comm = raw_input('Enter command #%s (rest, shield, move, shoot)' %(i+1))
            c = self.command(comm, i)
            commands.append(c)
            i += 1
            if c == 'clear all':
                commands = list()
                i = 0
            if c == 'cancel':
                i -= 1
        self.world.receive_commands(commands)
