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
from copy import deepcopy
from random import sample, random

class AI(User):
    def check_legal_command(self, command, state, suffix, targets):
        #returns True if command is legal
        if command in ['rest', 'shield']:
            return True
        if command.startswith('s') and command != 'shield':
            #params must be x, y tuple of target
            params = targets[command]
            tile = self.world.check_tile(*params)

        if command in 'uldr':
            #params must be (x, y, direction)
            x = state['x' + suffix]
            y = state['y' + suffix]
            if command == 'u':
                x -= 1
            if command == 'd':
                x += 1
            if command == 'r':
                y += 1
            if command == 'l':
                y -= 1
            tile = self.world.check_tile(x, y)

        if tile in ('NA', 'X'):
            return False
        else:
            return True

    def get_commands(self):
        state = self.world.get_state()
        state_ = self.extract_features(state)

        ####temporary naive AI rules just for testing purposes###
        # if state_['los']:
        #     commands = [Command(i, 'shoot', self.player, (state_['x_'], state_['y_'])) for i in range(3)]
        # else:
        #     commands = [Command(i, 'move', self.player, state_['gradient']) for i in range(3)]
        # self.world.receive_commands(commands)
        actions = self.build_tree(state_)
        commands = self.create_commands(actions)
        self.world.receive_commands(commands)




    def evaluate_state(self, state):
        #scores the game state. Higher scores are more advantageous
        score = state['health_diff']*self.params['health_diff']
        if state['health_diff'] >= 0:
            if state['los']:
                score += self.params['los_bonus']
        else:
            if state['los']:
                score -= self.params['los_bonus']
        if state['health_diff'] == 0:
            score -= state['dist']/float(self.params['dist_div'])
        #make it aggressively pursue a positive healthdiff
        if state['health_diff'] > 0:
            score += self.params['health_diff_aggress']
        if state['health_'] <= 0:
            score += self.params['win']
        if state['health'] <= 0:
            score += self.params['lose']
        return score

    def extract_features(self, state):
        #Takes raw game state and computes high level features
        #Examples might include whether there is a clear line of sight to opponent
        #Distance to opponent, distance to nearest barrier

        x = state['p%s_x' %self.id]
        y = state['p%s_y' %self.id]
        x_ = state['p%s_x' %(3 - self.id)]
        y_ = state['p%s_y' %(3 - self.id)]
        touched_cells = self.player.trace_ray((x,y), (x_, y_))
        los = (x_, y_) in touched_cells
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
            'health': health,
            'health_': health_,
            'health_diff': health_diff,
            'x': x,
            'y': y,
            'x_': x_,
            'y_': y_,
            'shield': False,
            'shield_': False
        }
        return out

    def build_tree(self, state):
        moves = [['rest', 'shield', 'u','d','l','r', 's', 'sr', 'sd', 'sl', 'su'],
            ['srr', 'srd', 'sdd', 'sld', 'sll', 'slu', 'suu', 'sru'],
            ['srrr', 'srrd', 'srdd', 'sddd', 'sldd', 'slld', 'slll', 'sllu', 'sluu', 'suuu', 'sruu', 'srru']
            ]
        orig_state = state
        shootings = moves[1] + moves[2] + moves[0][6:]
        targets1 = {s: (state['x_'] + s.count('d') - s.count('u'), state['y_'] + s.count('r') - s.count('l')) for s in shootings}
        targets2 = {s: (state['x'] + s.count('d') - s.count('u'), state['y'] + s.count('r') - s.count('l')) for s in shootings}

        def recurse(state, depth, alpha = -99, beta = 99):
            if depth == 3:
                return self.evaluate_state(state), []
            if depth == 0:
                moves_ = moves[0]
            if depth == 1:
                moves_ = moves[0] + moves[1]
            if depth == 2:
                moves_ = moves[0] + moves[1] + moves[2]
            sample_ = True #sample the moves because brute force is too much
            if sample_:
                m = moves_[:11]
                if depth > 0:
                    moves_ = m + sample(moves_[11:], 3)
            best_score = -99
            best_action = ''
            for m1 in moves_:
                n = 0
                tot_score = 0
                if not self.check_legal_command(m1, state, '', targets1):
                    continue
                min_score = 99
                min_action = ''
                for m2 in moves_:
                    if not self.check_legal_command(m2, state, '_', targets2):
                        continue
                    n += 1
                    state_ = self.update_state(state, m1, m2, orig_state, targets1, targets2)
                    score, actions = recurse(state_, depth + 1, alpha, beta)
                    tot_score += score
                    if score < min_score:
                        min_score = score
                        min_action = actions
                        #alpha-beta pruning
                        if min_score < beta:
                            beta = min_score
                        if beta < alpha:
                            break
                    elif score == min_score:
                        if random() < .25:
                            min_score = score
                            min_action = actions
                mean_score = tot_score/n
                min_score = mean_score
                if min_score > best_score:
                    best_score = min_score
                    best_action = [m1] + list(min_action)
                elif best_score == min_score:
                    if random() < .25:#break ties randomly
                        best_score = min_score
                        best_action = [m1] + list(min_action)
                if best_score > alpha:
                    alpha = best_score

            return best_score, best_action
        score, best_actions = recurse(state, 0)
        return best_actions

    def create_commands(self, actions):
        moves = [['rest', 'shield', 'u','d','l','r', 's', 'sr', 'sd', 'sl', 'su'],
            ['srr', 'srd', 'sdd', 'sld', 'sll', 'slu', 'suu', 'sru'],
            ['srrr', 'srrd', 'srdd', 'sddd', 'sldd', 'slld', 'slll', 'sllu', 'sluu', 'suuu', 'sruu', 'srru']
            ]
        state = self.extract_features(self.world.get_state())
        shootings = moves[1] + moves[2] + moves[0][6:]
        targets = {s: (state['x_'] + s.count('d') - s.count('u'), state['y_'] + s.count('r') - s.count('l')) for s in shootings}
        commands = list()
        for i in range(3):
            action = actions[i]
            if action in ('rest', 'shield'):
                c = Command(i, action, self.player)
            if action in 'udlr':
                c = Command(i, 'move', self.player, action)
            if action.startswith('s') and action != 'shield':
                c = Command(i, 'shoot', self.player, targets[action])
            commands.append(c)
        return commands


    def update_state(self, state, m1, m2, orig_state, targets1, targets2):
        #returns updated state
        state_ = deepcopy(state)
        state_['shield'] = False
        state_['shield_'] = False
        ms = [m1, m2]
        for i in range(2):
            suffix = ''
            if i == 1:
                suffix = '_'
            m = ms[i]
            if m == 'rest':
                if state_['health' + suffix] < 5:
                    state_['health' + suffix] += 0.25
            if m == 'shield':
                state_['shield' + suffix] = True
            if m == 'r':
                state_['y' + suffix] += 1
            if m == 'l':
                state_['y' + suffix] -= 1
            if m == 'u':
                state_['x' + suffix] -= 1
            if m == 'd':
                state_['x' + suffix] += 1
        #update LOS and dist
        x = state_['x']
        y = state_['y']
        x_ = state_['x_']
        y_ = state_['y_']
        touched_cells = self.player.trace_ray((x,y), (x_, y_))
        los = (x_, y_) in touched_cells
        dist = abs(x - x_) + abs(y - y_)
        state_['los'] = los
        state_['dist'] = dist

        for i in range(2):
            suffix = ''
            suffix_ = '_'
            if i == 1:
                suffix = '_'
                suffix_ = ''
            m = ms[i]
            if m.startswith('s') and m != 'shield':
                if i == 0:
                    x_targ, y_targ = targets1[m]
                else:
                    x_targ, y_targ = targets2[m]
                x = state_['x' + suffix]
                y = state_['y' + suffix]
                x_ = state_['x' + suffix_]
                y_ = state_['y' + suffix_]
                touched_cells = self.player.trace_ray((x, y), (x_targ, y_targ))
                if (x_, y_) in touched_cells:
                    if not state_['shield' + suffix_]:
                        state_['health' + suffix_] -= 1
        #update healthdiff
        state_['health_diff'] = state_['health'] - state_['health_']
        return state_






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
