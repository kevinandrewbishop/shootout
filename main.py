from board import Board
from player import Player
from world import World
from user import User
from command import Command



if __name__ == '__main__':
    barriers = [(2,2),(2,3),(2,4),(2,5),(3,2),(4,2),(5,2)]
    barriers += [(9-item[0],14-item[1]) for item in barriers]
    world = World((10,15))
    for b in barriers:
        x, y = b
        world.tiles[x][y] = 'X'
    user1 = User(world, 1)
    user2 = User(world, 2)

    while True:
        world.print_tiles()
        print "USER 1 COMMANDS"
        user1.get_commands()
        print "USER 2 COMMANDS"
        user2.get_commands()
        world.print_tiles()
        world.execute_logic()
