"""
Task description:

Suppose you have rectangular area of size M x N. On each field you have
0 or 1. Your task is to design algorithm and write Python function for
marking the largest 8-connected area of ones. Fields from the largest area
should have the value 2.

|1|0|1|0|1|    |2|0|2|0|1|
|1|1|1|0|0| => |2|2|2|0|0|
|0|1|0|1|0|    |0|2|0|2|0|
|0|1|0|0|0|    |0|2|0|0|0|

|1|0|1|     |2|0|2|
|0|1|0| =>  |0|2|0|
|0|0|0|     |0|0|0|

If there will be more than one such area then all should be marked:

|1|0|0|1|     |2|0|0|2|
|1|1|0|1| =>  |2|2|0|2|
|0|0|0|1|     |0|0|0|2|

With the code please provide time complexity of your algorithm
(use big O notation - http://en.wikipedia.org/wiki/Big_O_notation).

Your function should have the following signature:

- as a parameter it gets list of lists like:
    [
        [1,0,1,0,1],
        [1,1,1,0,0],
        [0,1,0,1,0]
    ]

- returns list of lists like:
    [
        [2,0,2,0,1],
        [2,2,2,0,0],
        [0,2,0,2,0]
    ]

The input parameter can be modified.
"""


def mark_largest_areas(matrix):
    """Task function implementation."""
    ConnectedAreasMarker(matrix)
    return matrix


class ConnectedAreasMarker(object):
    """Marks connected areas (as described in task description) in initial
    matrix just after object construction.

    Terms used:
        S = M x N - size of initial 1/0 matrix;
        K - number of 1 (ones) in matrix;
        A - constant in range 1 .. 9;
        cell - (x, y) - pair of indices;
        area - {cell, cell, ...} - set of cells.

    Algorithm summary:
        This is a typical connected components labeling graph problem.
        Nevertheless this algorithm works with sets of ones (areas)
        rather than with graph edges and vertices.

    Complexity analysis:
        Time:
            1. At first we should gather all one cells. This is O(S);
            2. Build initial areas of some size in range A (1..9)
               This is O(K);
            3. Merge neighbor areas and get disconnected separate areas
               This is about O(K^2) in worst case but with arerage case
               input it will perform much faster than this;
            4. Finally mark all largest areas. This is O(K).

            So worst case time complexity is quadratic polinomial
            (constants omitted): O(K^2 + K + S) => O(K^2)

            Algorithms performance strongly depends on input data so it could
            perform quite fast in some cases (like f.e. some quadratic
            time sorting algorithms in case of almost-sorted input).

        Space:
            As this algorithms is only interested in one cells and
            finally marks areas in initial matrix the space complexity is O(K)
            for areas storing in sets.
    """
    def __init__(self, matrix):
        self.matrix = matrix
        self.width = len(matrix[0])
        self.height = len(matrix)

        self.mark_matrix()

    def neighbor_one_cells(self, cell):
        x, y = cell
        return {(X, Y) for (X, Y) in (
                        (x, y - 1), # Up.
                        (x, y + 1), # Down.
                        (x - 1, y), # Left.
                        (x + 1, y), # Right.
                        (x - 1, y - 1), # Up-left.
                        (x + 1, y - 1), # Up-right.
                        (x - 1, y + 1), # Down-left.
                        (x + 1, y + 1)) if (# Down-right.
                            0 <= X < self.width and 0 <= Y < self.height and (
                                    self.is_one((X, Y))))}

    def is_one(self, cell):
        x, y = cell
        return self.matrix[y][x] == 1

    def all_one_cells(self):
        cells = set()
        for x in range(self.width):
            for y in range(self.height):
                cell = (x, y)
                if self.is_one(cell):
                    cells.add(cell)
        return cells

    def connected_areas(self):
        """Returns all 1..9-size areas of ones. Areas have no intersections."""
        areas = set()
        one_cells = self.all_one_cells()
        while one_cells:
            cell = one_cells.pop()
            neighbors = {
                    c for c in self.neighbor_one_cells(cell) if c in one_cells}
            current_area = {cell} | neighbors
            one_cells -= neighbors
            areas.add(frozenset(current_area))
        return areas

    def find_neighbor_areas(self, area, areas):
        neighbor_areas = set()
        for cell in area:
            neighbor_ones = self.neighbor_one_cells(cell)
            if neighbor_ones:
                for other_area in areas:
                    if neighbor_ones & other_area:
                        neighbor_areas.add(other_area)
        return neighbor_areas

    def merge_areas(self, areas):
        """Returns all separate (disconnected) areas by merging 1..9 areas."""
        separate_areas = set()
        while areas:
            area = areas.pop()
            neighbor_areas = self.find_neighbor_areas(area, areas)
            for neighbor_area in neighbor_areas:
                area |= neighbor_area
            if neighbor_areas:
                areas -= neighbor_areas
                areas.add(area)
                separate_areas.add(area)
        return separate_areas

    def cells_to_be_marked(self, areas):
        max_area_len = len(max(areas, key=len))
        areas = {a for a in areas if len(a) == max_area_len}
        cells = []
        for area in areas:
            cells.extend(area)
        return cells

    def mark_cells(self, cells):
        for x, y in cells:
            self.matrix[y][x] = 2

    def mark_matrix(self):
        """Runs all important algorithm parts end eventually marks
        larges connected areas in matrix.
        """
        areas = self.merge_areas(self.connected_areas())
        self.mark_cells(self.cells_to_be_marked(areas))
