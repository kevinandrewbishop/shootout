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

class AI():
    def __init__(self):
        pass

    def check_legal_move(self, move):
        #returns True if move is legal
        pass

    def evaluate_state(self, state):
        #scores the game state. Higher scores are more advantageous
        pass

    def extract_features(self, state):
        #Takes raw game state and computes high level features
        #Examples might include whether there is a clear line of sight to opponent
        #Distance to opponent, distance to nearest barrier
        pass

    def build_tree(self):
        pass
