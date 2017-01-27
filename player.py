'''
Actions include the following:
    1) rest
    2) shield up
    3) move (this can take on four values u/d/l/r for up down left right)
    4) shoot (this takes on x/y coordinates of the player's target)
'''


class Player():
    def __init__(self, world, id):
        '''
        '''
        self.world = world
        self.id = id
        self.shield_up = False
        self.health = 5

    def render(self):
        pass

    def rest(self, params = None):
        self.shield_up = False
        if self.health < 5:
            self.health += .25

    def shield(self, params = None):
        self.shield_up = True

    def move(self, params = None):
        self.shield_up = False
        self.world.tiles[self.x][self.y] = '' #clear old position
        if params == 'u':
            self.x -= 1
        if params == 'd':
            self.x += 1
        if params == 'r':
            self.y += 1
        if params == 'l':
            self.y -= 1
        self.world.tiles[self.x][self.y] = str(self.id) #add new position

    def shoot(self, params):
        self.shield_up = False
        touched_cells = self.trace_ray((self.x, self.y), params)
        target = self.world.check_tile(*touched_cells[-1])
        if target not in ['', 'NA', 'X']:
            target = int(target)
            self.world.players[target].get_shot()

    def trace_ray(self, source_pos, target_pos):
        '''
        For players to shoot, global positions of barriers and other players
        must be known.
        http://playtechs.blogspot.com/2007/03/raytracing-on-grid.html
        '''
        x0, y0 = source_pos
        x1, y1 = target_pos
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x = x0
        y = y0
        n = 1 + dx + dy
        if x1 > x0:
            x_inc = 1
        else:
            x_inc = -1
        if y1 > y0:
            y_inc = 1
        else:
            y_inc = -1
        error = dx - dy
        dx *= 2
        dy *= 2

        touched_cells = [(x, y)]
        hit_obstacle = False
        while not hit_obstacle:
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
            tile = self.world.check_tile(x, y)
            if tile != '':
                hit_obstacle = True
            if tile != 'NA':
                touched_cells.append((x, y))
        return touched_cells

    def get_shot(self):
        if not self.shield_up:
            self.health -= 1
            print 'Player %s shot! (Health: %s)' %(self.id, self.health)
        else:
            print 'Player %s shot! But shield was up!' %(self.id)
