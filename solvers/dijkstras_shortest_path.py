class DijkstrasMazeSolver(object):
    """Gets shortest maze path with help of Dijkstras algorithm.
    It converts 0/1 matrix maze to graph representation
    and then finds shortest path. Also it uses Heap data structure.
    """
    def __init__(self, input_maze=None, is_graph=False):
        pass

class MazeToGraphConverter(object):
    """Converts 0/1 matrix maze to simplified graph perpesentation.
    f.e.:

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1,(N),0, 0, 0, 1, 1, 1, 0, 1, 1, 1],    N = 0
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

                                           Simplified graph:

                                                       (D) 
    Simplified maze (graph inside):                     #
                                                        #
    +----------------+-------------+                    #
    |(A)############ | ########### |       (A)###(B)###(C)
    |   +--------+ # + # +-----+ # |                    #
    |             (B)#(C)| ####### |                    #
    +----------------+ # | # +-----+                    #
                     |(D)|(F)###(J)|       (Q)   (J)###(F)
    +----------------+---+ # +-----+        #           # 
    |(Q)##(O)#(P)#(K)####### |              #           #
    +----+ # + # + # +-------+              #           #
         | # | # | # |                     (O)###(P)###(K)
         |(L)|(M)|(N)|                      #     #     #
         +---+---+---+                      #     #     #
                                            #     #     #
                                           (L)   (M)   (N)
    """
    def __init__(self, maze):
        pass

    def maze_matrix_to_graph(maze):
        """Simplifies graph (merge edges / remove vertex) if possible."""
        self.maze_height = len(maze)
        self.maze_width = len(maze[0])
        pass

    def near_cells(self, x, y):
        return {
            'U' : (x, y - 1), # up
            'R' : (x + 1, y), # right
            'D' : (x, y + 1), # down
            'L' : (x - 1, y)  # left
        }

    def can_go(self, x, y, direction):
        x1, y1 = self.near_cells(x, y)[direction]
        if 0 <= x1 < self.maze_width and 0 <= y1 < self.maze_height:
            return self.maze[y1][x1] == 0
        else:
            return False

    def possible_moves(self, x, y):
        return ''.join([d for d in 'URLD' if self.can_go(x, y, d)])



class MazeSolver:
    '''
    Recursively calculates exit routes without "turing back".
    if 'search_all' is set it will produce multiple exit routes but can cause
    an infinite loop.
    '''

    def __init__(self, maze, search_all = False):
        self.maze = maze
        self.routes = []
        self.search_all = search_all
        self.found = False

    def near_cells(self, x, y):
        return {
            'N' : (x, y - 1),
            'E' : (x + 1, y),
            'S' : (x, y + 1),
            'W' : (x - 1, y)
        }

    def can_go(self, x, y, direction):
        x1, y1 = self.near_cells(x, y)[direction]
        if 0 <= x1 <= 11 and 0 <= y1 <= 11:
            return self.maze[y1][x1] == 0
        else:
            return False

    def possible_moves(self, x, y):
        return ''.join([d for d in 'ENSW' if self.can_go(x, y, d)])

    def make_route(self, x, y, route, visited):
        if not self.found or self.search_all:
            for move in self.possible_moves(x, y):
                cell = self.near_cells(x, y)[move]
                if cell not in visited:
                    _route = route + [move]
                    _visited = visited + [cell]
                    # WIN!
                    if cell == (10, 10):
                        self.found = True
                        self.routes.append(''.join(_route))
                    else:
                        self.make_route(cell[0], cell[1], _route, _visited)
                        
    def solve(self):
        if not self.routes:
            self.make_route(1, 1, [], [(1, 1)])
        # return shortest
        return min(self.routes, key = len)
        
def solve_maze(data):
    return MazeSolver(data).solve()

#This code using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    print(solve_maze([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]))
    print(solve_maze([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]))
    #be careful with infinity loop
    print(solve_maze([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]))
    print(solve_maze([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]))
    print(solve_maze([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]))
