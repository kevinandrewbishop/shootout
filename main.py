from board import Board
from player import Player
from world import World
from user import User
from command import Command
from ai import AI
from random import random
from copy import deepcopy

if __name__ == '__main__':
    log_file = 'log_alphabeta1'
    params = {'health_diff': 1,
        'los_bonus': 1,
        'dist_div': 20.,
        'health_diff_aggress': 1,
        'win': 5,
        'lose': -5
        }
    barriers = [(2,2),(2,3),(2,4),(2,5),(3,2),(4,2),(5,2)]
    barriers += [(9-item[0],14-item[1]) for item in barriers]
    for i in range(25):
        param1 = deepcopy(params)
        for p in param1:
            r = random()
            if p == 'dist_div':
                r *= 8
            param1[p] += r
        param2 = deepcopy(params)
        for p in param2:
            r = random()
            if p == 'dist_div':
                r *= 8
            param2[p] += r
        world = World((10,15))
        for b in barriers:
            x, y = b
            world.tiles[x][y] = 'X'
        user1 = AI(world, 1, param1)
        user2 = AI(world, 2, param2)
        #user2 = User(world, 2)

        world.run()
        with open(log_file, 'a') as f:
            f.write('Iteration %s' %i)
            f.write('\n')
            f.write(str(param1))
            f.write('\n')
            f.write(str(param2))
            f.write('\n')
            f.write(str(world.get_state()))
            f.write('\n')
            f.write(str(world.round))
            f.write('\n')
