'''
Let's play a game of hide and seek. You have been given a map of 10x10 cells
and in one of the cells we've hidden your goal. You can move to and from any
cell in the field. On each move you'll get informed if the move places you
closer or further away from your goal, compared to your previous location. Your
function compiles data about previous steps, each step is a list of list, where
first and second elements are your coordinates (row and column) and third is
the info on how much closer you've gotten (colder or warmer) -- "colder" is -1,
"warmer" is 1 and "same" is 0. For your measurement of the distance to the goal
you should use the Euclidean distance. At each step you need to return the
coordinates for your next step. If your step places you within the goal cell,
then you win! You should find the goal within 12 steps.
'''

from math import hypot

r_10 = range(10)
all_cells = {(x, y) for x in r_10 for y in r_10}
discarded_cells = set()

def distance(cell_1, cell_2):
    x_1, y_1 = cell_1
    x_2, y_2 = cell_2
    return hypot(x_2 - x_1, y_2 - y_1)

def next_move(steps):
    global discarded_cells
    discarded_cells.add(tuple(steps[-1][:2]))

    if len(steps) > 1:
        pre_last_step_cell = steps[-2][:2]
        last_step_cell = steps[-1][:2]
        last_step_res = steps[-1][2]

        def condition(cell):
            d_1 = distance(pre_last_step_cell, cell)
            d_2 = distance(last_step_cell, cell)
            return d_1 < d_2 if last_step_res > 0 else d_1 > d_2

        discarded_cells |= {cell for cell in all_cells - discarded_cells if (
                                                            condition(cell))}
                                                            
    return (all_cells - discarded_cells).pop()

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    print(next_move([[2, 2, 0]]))  # [0, 2]
    print(next_move([[2, 2, 0], [0, 2, -1]]))  # [3, 2]
    print(next_move([[2, 2, 0], [0, 2, -1], [3, 2, 1]]))  # [4, 1]
    print(next_move([[2, 2, 0], [0, 2, -1], [3, 2, 1], [4, 1, 0]]))  # [3, 1]
