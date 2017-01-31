'''
Artificial Intelligence behind the computer player.
I'm borrowing what I can from chess engines.

Overall it basically does the following:
1) Request current game state from the World
2) Calculate tree of valid moves N moves ahead (not all possible moves, but
    a subtree of possible moves that look most promising. E.g. alfa-beta search).
    Nodes are game states and edges are moves (by both the player and opponent
    since moves are simultaneous).
3) Evaluate each node.
4) Choose the best leaf node and work backwards to the root to find best p1_health

This will have to somehow involve modeling opponent moves. A naive start would
be to assume opponent makes random choices mixed with simplistic heuristics.
'''
from config import NUM_ACTIONS, VALID_ACTIONS
from user import User
from command import Command

class AI(User):
    def check_legal_command(self, command, params = None):
        #returns True if command is legal
        if command in ['rest', 'shield']:
            return True
        if command == 'shoot':
            #params must be x, y tuple of target
            tile = self.world.check_tile(*params)

        if command == 'move':
            #params must be (x, y, direction)
            x, y, direction = params
            if direction == 'u':
                x -= 1
            if direction == 'd':
                x += 1
            if direction == 'r':
                y += 1
            if direction == 'l':
                y -= 1
            tile = self.world.check_tile(x, y)

        if tile == 'NA':
            return False
        else:
            return True

    def get_commands(self):
        state = self.world.get_state()
        state_ = self.extract_features(state)

        ####temporary naive AI rules just for testing purposes###
        if state_['los']:
            commands = [Command(i, 'shoot', self.player, (state_['x_'], state_['y_'])) for i in range(3)]
        else:
            commands = [Command(i, 'move', self.player, state_['gradient']) for i in range(3)]
        self.world.receive_commands(commands)




    def evaluate_state(self, state):
        #scores the game state. Higher scores are more advantageous
        pass

    def extract_features(self, state):
        #Takes raw game state and computes high level features
        #Examples might include whether there is a clear line of sight to opponent
        #Distance to opponent, distance to nearest barrier

        x = state['p%s_x' %self.id]
        y = state['p%s_y' %self.id]
        x_ = state['p%s_x' %(3 - self.id)]
        y_ = state['p%s_y' %(3 - self.id)]
        touched_cells = self.player.trace_ray((x,y), (x_, y_))
        los = touched_cells[-1] == (x_, y_)
        dist = abs(x - x_) + abs(y - y_)
        if abs(x - x_) > abs(y - y_):
            if x > x_:
                gradient = 'u'
            else:
                gradient = 'd'
        elif y > y_:
            gradient = 'l'
        else:
            gradient = 'r'

        health = state['p%s_health' %self.id]
        health_ = state['p%s_health' %(3 - self.id)]
        health_diff = health - health_
        out = {
            'los': los,
            'dist': dist,
            'gradient': gradient,
            'heath_diff': health_diff,
            'x': x,
            'y': y,
            'x_': x_,
            'y_': y_
        }
        return out

    def build_tree(self):
        pass



if __name__ == '__main__':
    from world import World
    barriers = [(2,2),(2,3),(2,4),(2,5),(3,2),(4,2),(5,2)]
    barriers += [(9-item[0],14-item[1]) for item in barriers]
    world = World((10,15))
    for b in barriers:
        x, y = b
        world.tiles[x][y] = 'X'
    user1 = AI(world, 1)
    user2 = User(world, 2)
