#! /usr/bin/python

from heap import PriorityQueue

class DijkstrasMazeSolver(object):
    """Gets shortest maze exit path with help of Dijkstras algorithm.
    It converts 0/1 matrix maze to edge weighted graph representation
    (due to MazeToGraphConverter) and then finds shortest path.
    Also it uses Heap data structure to quickly get minimums.
    """
    infinity = 10**10

    def __init__(self, input_maze=None):
        is_text = type(input_maze) == str
        if is_text:
            converter = TextToMatrixMazeConverter(input_maze)
            converter = MazeToGraphConverter(converter.maze,
                                             converter.start_cell)
        else:
            converter = MazeToGraphConverter(input_maze)

        self.vertices = converter.graph_vertices
        self.edge_weights = converter.graph_edge_weights
        self.adjacency_list = converter.graph_adjacency_list
        self.edge_weights = converter.graph_edge_weights
        self.start_v = converter.start_cell
        self.exit_v = converter.exit_cell
        self.dist = dict()
        self.prev = dict()
        self.queue = PriorityQueue()
        self.shortest_path = self.shortest_exit_path()

    def shortest_exit_path(self):
        self.count_shortest_paths(self.start_v)
        length = self.dist[self.exit_v]
        path = self.get_path(self.exit_v)
        return path, length
                
    def get_path(self, v, path=()):
        path = (v,) + path 
        if self.prev[v] and v != self.start_v:
            return self.get_path(self.prev[v], path)
        else:
            return path
         
    def count_shortest_paths(self, source):
        self.dist[source] = 0
        self.prev[source] = None

        for v in self.vertices:
            if v != source:
                self.dist[v] = self.infinity
                self.prev[v] = None
            else:
                self.queue.insert((v, self.dist[v]))

        while self.queue:
            u = self.queue.pop_min()[0]
            for v in self.adjacency_list[u]:
                edge = frozenset((u, v))
                alt = self.dist[u] + self.edge_weights[edge]
                if alt < self.dist[v]:
                    self.dist[v] = alt
                    self.queue.insert((v, alt))
                    self.prev[v] = u


class MazeToGraphConverter(object):
    """Converts 0/1 matrix maze to simplified edge weighted graph
    representation.

    11x11 maze example:

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],   (1, 1) = 0 <-- start cell
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],   (1, 6) = 2 <-- exit cell
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    maze_with_nodes = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1,(A),0, 0, 0, 1, 0, 0, 0, 0, 0, 1],   (A) = (1, 1) <-- start cell
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0,(B),0,(C),1, 1, 1, 0, 1],   (B) = (4, 4); (C) = (6, 4)
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1,(E),0, 0, 0, 1, 1, 1, 0, 1, 1, 1],   (E) = (1, 6) <-- exit cell
        [1, 1, 1, 1,(K),0, 0, 0,(F),0, 0, 1],   (K) = (4, 7); (F) = (8, 7)
        [1,(Q),1, 1, 0, 1, 1, 1, 1, 1,(J),1],   (Q) = (1, 8); (J) = (10, 8)
        [1,(O),0, 0,(P),0, 0, 0, 0, 1, 1, 1],   (O) = (1, 9); (P) = (4, 9)
        [1,(L),1, 1, 1, 1, 1, 1, 0, 0,(M),1],   (L) = (1, 10); (M) = (10, 10)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  
    ]                                            Nodes are:
                                                    - start cell;
                                                    - exit cell;
                                                    - dead end cells;
                                                    - 3 and 4 way crossings.


                                           Simplified weighted graph:

                                                       (D) 
    Simplified maze (graph inside):    start vertex     #
                                            |           #
    +----------------+-------------+        V           #
    |(A)############ | ########### |       (A)###(B)###(C)
    |   +--------+ # + # +-----+ # |                    #
    |             (B)#(C)| ####### |                    # <-- each edge is
    +----------------+ # | # +-----+                    #     weighted with
                     |(D)|(F)###(J)|       (Q)   (J)###(F)    actual number
    +----------------+---+ # +-----+        #           #     of cells
    |(Q)##(O)#(P)#(K)####### |              #           #     between nodes
    +----+ # + # + # +-------+              #           #     + 1:
         | # | # | # |                     (O)###(P)###(K)     W(C, F) = 15
         |(L)|(M)|(E)|                      #     #     #
         +---+---+---+                      #     #     #
                                            #     #     #
                                           (L)   (M)   (E) <-- exit vertex


    So the shortest (A) -> (E) path will      be      of      TOTAL LENGTH:

         (A)  ->  (B)  ->  (C)  ->  (F)  ->  (K)  ->  (E)          ||
    [or]                                                           ||
        (1,1) -> (4,4) -> (6,4) -> (8,7) -> (4,7) -> (1,6)         ||
    [edge     ||       ||       ||       ||       ||
     weights]: 6   +    2   +   15   +    4    +   4       =       31 
    """
    def __init__(self, maze, start_cell=(1, 1)):
        self.graph_vertices = set()
        self.graph_edge_weights = dict() # weighted edges
        self.graph_adjacency_list = dict()
        self.maze_height = len(maze)
        self.maze_width = len(maze[0])
        self.maze = maze
        self.start_cell = start_cell
        self.exit_cell = None
        self.make_graph()

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
            return self.maze[y1][x1] != 1
        else:
            return False

    def possible_moves(self, x, y):
        return ''.join([d for d in 'DRUL' if self.can_go(x, y, d)])

    def make_vertices_and_edges(self, x, y, visited):
        # print x, y
        if not self.exit_cell and self.maze[y][x] > 1:
            self.exit_cell = (x, y)
        possible_moves = self.possible_moves(x, y)
        if (len(visited) == 1 # start vertex
                ) or (len(possible_moves) in (
                    1, # dead end
                    3, # 3-way crossing
                    4) # 4-way crossing
                        ) or (x, y) == self.exit_cell: # exit vertex
            self.graph_vertices.add((x, y))
            for i, (x1, y1) in enumerate(visited):
                if (x, y) != (x1, y1) and (x1, y1) in self.graph_vertices:
                    edge = frozenset([(x, y), (x1, y1)])
                    if (not edge in self.graph_edge_weights) or (
                                    self.graph_edge_weights[edge] > i + 1):
                        self.graph_edge_weights[edge] = i + 1
                    break
        for move in possible_moves:
            cell = self.near_cells(x, y)[move]
            if cell not in visited:
                visited = ((x, y),) + visited
                self.make_vertices_and_edges(*cell, visited=visited)

    def make_adjacency_list(self):
        for v in self.graph_vertices:
            for e in self.graph_edge_weights:
                if v in e:
                    u = set(e - {v}).pop()
                    self.graph_adjacency_list[v] = (
                                self.graph_adjacency_list.get(v, []) + [u])

    def make_graph(self):
        start = self.start_cell
        self.make_vertices_and_edges(*start, visited=(start,))
        if not self.exit_cell:
            raise Exception('Exit cell (2) not found in maze!')
        self.make_adjacency_list()


class TextToMatrixMazeConverter(object):
    """Converts text-maze to matrix 0/1 maze.
    Example:

    XXXXX      [ [1, 1, 1, 1, 1],
    X S X        [1, 0, 0, 0, 1],
    X   X   ==>  [1, 0, 0, 0, 1],
    X XXX        [1, 0, 1, 1, 1],
    X E X        [1, 0, 2, 0, 1],
    XXXXX        [1, 1, 1, 1, 1] ]
    """
    def __init__(self, maze):
        self.maze_to_matrix(maze)

    def maze_to_matrix(self, maze):
        self.maze = []
        self.start_cell = None
        for li, line in enumerate(maze.split('\n')):
            maze_line = []
            for ci, char in enumerate(line):
                if char.upper() == 'S':
                    maze_line.append(0)
                    self.start_cell = (ci, li)
                elif char.upper() == 'E':
                    maze_line.append(2)
                elif char.isspace():
                    maze_line.append(0)
                else:
                    maze_line.append(1)
            self.maze.append(maze_line)


if __name__ == '__main__':
    # ATTENTION:
    # running all those tests could require 5-15 seconds.
    maze = ('######\n'
            '# S  #\n'
            '#### #\n'
            '#    #\n'
            '# ####\n'
            '#    #\n'
            '## ###\n'
            '## ###\n'
            '#   E#\n'
            '######')

    assert DijkstrasMazeSolver(maze).shortest_path == (
                ((2, 1), (2, 5), (2, 8), (4, 8)), 15) # path, len(path)

    # takes a bit long time due to rooms
    maze = ('XXX+-+-----------------------+\n'
            'XXX| |                       |\n'
            'XXX| +===+ +=+ +=+ +-+-->    |\n'
            '+--^ |S    | | | | | |       |\n'  # S - start
            '|    +--+--+ | | | | | <-+===+\n'
            '+-----+ |    | | | | |   \WWWW\n'
            '|       |    +-+ +-+ V <-+===+\n'
            '| <=====+=+                  |\n'
            '|            _.-+ +--+ .._/^^~\n'
            '+=====+->   /~~~|E|~~| |~~~~~~\n'  # E - exit
            ' }O_o{|     |~~~+-+~~+~+~~~~~~\n'
            '  ^^^ |_/\__/~~~~~~~~~~~~~~~~~\n')
            
    assert DijkstrasMazeSolver(maze).shortest_path == (
        ((6, 3), (10, 1), (14, 1), (18, 1), (25, 1), (25, 2), (25, 3),
         (22, 5), (22, 7), (20, 7), (17, 7), (17, 9)), 37)

    # example from MazeToGraphConverter's docstr:
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 2 ,0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    assert DijkstrasMazeSolver(maze).shortest_path == (
            ((1, 1), (4, 4), (6, 4), (8, 7), (4, 7), (1, 6)), 31) # path, len

    maze = [
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
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    assert DijkstrasMazeSolver(maze).shortest_path == (
            ((1, 1), (1, 6), (3, 6), (4, 7), (6, 7), (8, 8), (10, 10)), 18)

    # one room maze (infinite loop test)
    maze = [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 1],
        [1, 1, 1, 1, 1, 1],
    ]
    assert DijkstrasMazeSolver(maze).shortest_path == (
                    ((1, 1), (2, 1), (2, 2), (2, 3), (3, 3),
                     (3, 4), (3, 5), (3, 6), (4, 6)), 8)

    # one room maze with walls (infinite loop test)
    maze = [
        [1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 2, 1],
        [1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
    assert DijkstrasMazeSolver(maze).shortest_path == (
                ((1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 2), (5, 1)), 8)
