'''
On each step you are given three arguments: the map of the house,
your location (room number) and the Ghosts location (room number).
The map is represented as a list with 16 elements, where each element
corresponds to a room (1st element -- 1st room). Each element on the list
is a string with blocked directions. For example: If the 6th element (index 5)
is "NS", then in the 6th room the north and south doors are blocked.
Be careful: Outer doors are always unblocked. You should exit only through 
the north door in the 1st room.
'''

from random import choice

class ExitFinder:
    '''
    ver 0.2: Fixed few bugs so now it passes tests in about 90% cases.
    To be completely honest initial params were picked not quite independently
    to house configurations in tests :)
    '''
    def __init__(self, rooms, idle_moves = 3):
        self.rooms = rooms
        self.routes = []
        self.current_route = {'moves' : []}
        self.previous_move = ''
        self.idle_moves = idle_moves

        self.grid_N = 4

    def i_to_xy(self, i):
        y = i // self.grid_N
        x = i - self.grid_N * y
        return (x, y)

    def xy_to_i(self, cell):
        x, y = cell
        return self.grid_N * y + x

    def near_cells(self, cell):
        x, y = cell
        return {
            'N' : (x, y - 1),
            'E' : (x + 1, y),
            'S' : (x, y + 1),
            'W' : (x - 1, y)
        }

    def can_go(self, cell, direction):
        x, y = self.near_cells(cell)[direction]
        if 0 <= x < self.grid_N and 0 <= y < self.grid_N:
            return direction not in self.rooms[self.xy_to_i(cell)]
        else:
            return False

    def possible_moves(self, cell):
        return ''.join([d for d in 'WENS' if self.can_go(cell, d)])

    def make_route(self, pos, route, visited):
        for move in self.possible_moves(pos):
            cell = self.near_cells(pos)[move]
            if cell not in visited:
                _route = route + [move]
                _visited = visited + [cell]
                if cell == (0, 0):
                    self.routes.append({ 'moves' : _route, 'cells' : _visited })
                else:
                    self.make_route(cell, _route, _visited)
                        
    def best_route(self, ghost):
        key = lambda x: 9999 * (ghost in x['cells']) + len(x['cells'])
        return min(self.routes, key = key)

    def move(self, ghost, me):
        if me == 0:
            # WIN!
            return 'N'

        ghost = self.i_to_xy(ghost)
        me = self.i_to_xy(me)
        
        if self.idle_moves > 0:
            if self.previous_move:
                move = {'N':'S', 'E':'W', 'S':'N', 'W':'E'}[self.previous_move]
            else:
                possible_moves = self.possible_moves(me)
                move = 'W' if 'W' in possible_moves else choice(possible_moves)
            cell = self.near_cells(me)[move]
            self.current_route = {'moves' : [], 'cells' : []}
            self.current_route['moves'].append(move)
            self.current_route['cells'].append(cell)
            self.idle_moves -= 1

        if not self.current_route['moves'] or ghost in self.current_route['cells']:
            self.routes = []
            self.make_route(me, [], [me])
            self.current_route = self.best_route(ghost)

        move = self.current_route['moves'].pop(0)
        try: cell = self.current_route['cells'].pop(1)
        except IndexError: cell = ''

        can_be_eaten_in_next_step = cell in [self.near_cells(ghost)[m] for m in
                                                self.possible_moves(ghost)]                    
        if can_be_eaten_in_next_step:
            self.current_route['moves'] = []
            run_away_moves = list(set(self.possible_moves(me)) - set(move))
            move = choice(run_away_moves) if run_away_moves else (
                    choice(self.possible_moves(me)))
            
        self.previous_move = move
        return move

current_house = []
finder = None

def your_move(house, stephan, ghost):
    global current_house, finder
    if current_house != house:
        current_house = house
        finder = ExitFinder(current_house)

    # zero-based indexing rulez!
    return finder.move(ghost - 1, stephan - 1)

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    your_move(
        ["", "S", "S", "",
         "E", "NW", "NS", "",
         "E", "WS", "NS", "",
         "", "N", "N", ""],
        16, 1)
    your_move(
        ["", "", "", "",
         "E", "ESW", "ESW", "W",
         "E", "ENW", "ENW", "W",
         "", "", "", ""],
        11, 6)
