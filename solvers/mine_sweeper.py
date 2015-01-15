class MineSweeper:
    '''
    Solution uses sets heavily thus is quite elegant (IMHO)
    but is definitely not the fastest and most optimized one.
    '''
    def __init__(self, field):
        self.field = field
        self.field_N = len(field[0])
        
        range_N = range(self.field_N)
        
        self.cells = {(x, y) for y in range_N for x in range_N if (
                                        self.number((x, y)))}
                                        
        self.unknown_cells = {c for c in self.cells if self.number(c) < 0}
        
        self.result = (False, 0, 0) if (
                            len(self.unknown_cells) == self.field_N ** 2) else (
                            self.decision())

    def is_cell(self, cell):
        x, y = cell
        return 0 <= x < self.field_N and 0 <= y < self.field_N
            
    def near_cells(self, cell):
        x, y = cell
        return set(filter(self.is_cell, (
                        (x, y - 1),
                        (x + 1, y),
                        (x, y + 1),
                        (x - 1, y),
                        (x + 1, y - 1),
                        (x + 1, y + 1),
                        (x - 1, y - 1),
                        (x - 1, y + 1)
                        )))
    
    def number(self, cell):
        x, y = cell
        return self.field[y][x]

    def decision(self):
        numbered_cells = {(self.number(c), c) for c in (
                                    self.cells - self.unknown_cells) if (
                                    self.number(c) < 9)}
                                
        mined_cells = {c for c in self.cells - self.unknown_cells if (
                                    self.number(c) == 9)}
                                    
        for value, cell in numbered_cells:
            near = self.near_cells(cell)
            near_mined_cells = near & mined_cells
            near_unknown_cells = near & self.unknown_cells
            if near_unknown_cells:
                near_unknown_N = len(near_unknown_cells)
                near_mined_N = len(near_mined_cells)
                cell = near_unknown_cells.pop()
                x, y = cell
                if value == near_unknown_N + near_mined_N:
                    return (True, y, x)
                elif value == near_mined_N:
                    return (False, y, x)
        
def mine_sweeper(field):
    return MineSweeper(field).result

if __name__ == '__main__':
    #These are just examples
    mine_sweeper([
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ])  # [False, 0, 0]
    mine_sweeper([
        [0, 2, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 2, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 1, 1, 1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 1, -1, -1, -1, -1, -1, -1],
        [0, 1, 1, 2, -1, -1, -1, -1, -1, -1],
        [0, 1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 1, -1, -1, -1, -1, -1, -1, -1, -1],
        [2, 1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ])  # [True, 0, 2]
