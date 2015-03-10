#! /usr/bin/python

class DijkstrasMazeSolver(object):
    """Gets shortest maze path with help of Dijkstras algorithm.
    It converts 0/1 matrix maze to edge weighted graph representation
    (due to MazeToGraphConverter) and then finds shortest path.
    Also it uses Heap data structure to quickly get minimums.
    """
    def __init__(self, input_maze=None, is_graph=False):
        if not is_graph:
            converter = MazeToGraphConverter(input_maze)
            self.vertices = converter.greph_vertices
            self.edge_weights = converter.greph_edge_weights

    def shortest_path(self):
        pass



class MazeToGraphConverter(object):
    """Converts 0/1 matrix maze to simplified edge weighted graph
    perpesentation.
    f.e.:

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    maze_with_nodes = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1,(A),0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0,(B),0,(C),1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1,(E),0, 0, 0, 1, 1, 1, 0, 1, 1, 1],   (E) = 0: exit cell
        [1, 1, 1, 1,(K),0, 0, 0,(F),0, 0, 1],
        [1,(Q),1, 1, 0, 1, 1, 1, 1, 1,(J),1],    Nodes are:
        [1,(O),0, 0,(P),0, 0, 0, 0, 1, 1, 1],     - start point;
        [1,(L),1, 1, 1, 1, 1, 1, 0, 0,(M),1],     - dead ends;
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],     - 3 and 4 way crossings.
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
         |(L)|(M)|(E)|                      #     #     #
         +---+---+---+                      #     #     #
                                            #     #     #
                                           (L)   (M)   (E) <-- exit vertex
    """
    def __init__(self, maze):
        self.graph_vertices = set()
        self.graph_edge_weights = dict() # weighted edges
        self.maze_height = len(maze)
        self.maze_width = len(maze[0])
        self.maze = maze
        self.make_graph(1, 1, ((1, 1),))

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

    def make_graph(self, x, y, visited):
        possible_moves = self.possible_moves(x, y)
        if (len(visited) == 1 # start vertex
                ) or len(possible_moves) in (
                    1,  # dead end
                    3,  # 3-way crossing
                    4): # 4-way crossing
            self.graph_vertices.add((x, y))
            for i, (x1, y1) in enumerate(visited):
                if (x, y) != (x1, y1) and (x1, y1) in self.graph_vertices:
                    edge = frozenset([(x, y), (x1, y1)])
                    if not edge in self.graph_edge_weights:
                        self.graph_edge_weights[edge] = i + 1
                    break
        for move in possible_moves:
            cell = self.near_cells(x, y)[move]
            # print visited
            if cell not in visited:
                visited = ((x, y),) + visited
                xc, yc = cell
                self.make_graph(xc, yc, visited)

#This code using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0 ,0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    m2g = MazeToGraphConverter(maze)
    m2g.make_graph(1, 1, ((1, 1),))
    print m2g.graph_vertices
    print m2g.graph_edge_weights


    '''
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
'''
