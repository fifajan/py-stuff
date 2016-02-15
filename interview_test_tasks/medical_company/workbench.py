# (c) Alexey Ivchenko (yanepman@gmail.com), 2015

class Workbench(object):
    """Represents workbench for crafting stuff from items via recipes."""

    def __init__(self, max_print_size=77):
        # max_print_size is picked as 77 to represent
        # standard terminal window size.
        self.items_count = 0
        self.max_print_size = max_print_size
        self.clear()

    def max_indices(self):
        all_indices = {i_j for places in self.grid.values() for i_j in places}
        max_i = max(i for i, j in all_indices) if all_indices else -1
        max_j = max(j for i, j in all_indices) if all_indices else -1
        return (max_i, max_j)

    def new_meth(self):
        print 'HELLO, '
        print 'WORLD!'

    def clear(self):
        """Clears workbench grid (inventory)."""
        # Sparse grid approach were used here:
        # we store only occupied positions
        # so we don't waste memory for nil positions.
        # Refer to 'Recipe' __init__ docstr for 
        # container format description.
        self.grid = dict()
        self.items_count = 0

    def add_item(self, item, position):
        """Adds one item at given position."""
        if not Recipe.is_valid_position(position):
            raise IndexError('Incorrect grid index.')
        position_is_occupied = any(
                position in places for places in self.grid.values())
        if not position_is_occupied:
            self.items_count += 1
        if self.grid.get(item):
            self.grid[item] |= set([position])
        else:
            self.grid[item] = set([position])

    def add_recipe_items(self, recipe):
        """Updates grid with items at places provided in recipe dict format."""
        recipe.optimize_position()
        for item, places in recipe.items.items():
            self.grid[item] = places

        self.items_count = self.get_items_count()

    def get_items_count(self):
        """Returns total count of items (ingredients) in workbench."""
        return sum(1 for places in self.grid.values() for pos in places)

    def craft(self, recipe_name=None):
        """Tries to craft something.

        Returns recipe name if crafting succeded or None otherwise.
        """
        if not recipe_name:
            for recipe_name, recipe in CorrectRecipes.recipes.items():
                if self.grid == recipe.items:
                    return recipe_name
        else:
            recipe = CorrectRecipes.recipes.get(recipe_name)
            if not recipe:
                raise KeyError("Recipe '%s' not found" % recipe_name)
            else:
                if self.grid == recipe.items:
                    return recipe_name

    def __len__(self):
        return self.items_count

    def __repr__(self):
        max_i, max_j = self.max_indices()
        if max_i > self.max_print_size or max_j > 2 * self.max_print_size:
            return 'Workbench is too big to print it!'

        result = []
        for j in range(max_j + 1):
            result.append([])
            for i in range(max_i + 1):
                result[j].append(' ')

        for item, places in self.grid.items():
            for i, j in places:
                result[j][i] = item

        border = '+' + ('-' * (max_i + 1)) + '+'
        str_result = border + '\n'
        if result:
            str_result += '\n'.join('|'+ ''.join(row) + '|' for row in result)
        else:
            str_result += '||'
        str_result += '\n' + border

        return str_result


    def __str__(self):
        return repr(self)

class Recipe(object):
    """Represents recipe that could be crafted using Workbench."""

    @staticmethod
    def is_valid_position(position):
        """Checks if position indices are valid integers"""
        try:
            i, j = position
            int(i), int(j)
        except (ValueError, TypeError):
            return False
        return True

    def __init__(self, items):
        """Items is a followind kind of dict {str - key : set of tuples - val,}

        { 'A' : {(0, 0)}, 'B' : {(1, 1)}, 'C': {(1, 0), (2, 0)} }

        Key is an item, value is a set of indexed positions where item lies.
        """
        self.items = items
        self.name = ''
        self.count = self.get_count()
        self.is_optimized = False

    def optimize_position(self):
        """Tries to shift all items to (0, 0) origin position.

        In addition it validates indices and raises IndexError in bad cases.
        """
        min_i = min_j = 10**20
        for item, places in self.items.items():
            for i, j in places:
                if Recipe.is_valid_position((i, j)):
                    min_i = min(min_i, i)
                    min_j = min(min_j, j)
                else:
                    raise IndexError('Incorrect grid index.')

        if min_i or min_j:
            for item, places in self.items.items():
                optimized_places = set()
                for i, j in places:
                    optimized_places.add((i - min_i, j - min_j))
                self.items[item] = optimized_places

        self.is_optimized = True

    def get_name(self):
        """Checks if this recipe could be crafted.

        If recipe is invalid then returns None.
        """
        if self.name:
            return self.name
        for name, recipe in CorrectRecipes.recipes.items():
            if recipe.items == self.items:
                self.name = name
                return name

    def get_count(self):
        """Returns total count of items in recipe."""
        return sum([len(positions) for positions in self.items.values()])

    def __len__(self):
        return self.count

class CorrectRecipes():
    """Represents dict of correct recipes which could be crafted.

    This is a static class.
    Singletone pattern is used here.
    """

    def generate_long_sword():
        long_sword = { 'W' : {(0, 0)} } # grip
        long_blade = {(i, i) for i in range(1, 10**5)}
        long_sword.update({'I' : long_blade})
        return long_sword
                                                # How those recipes will look
                                                # in workbench:
    recipes = {                                 # ---------------------------
        'torch' : Recipe( {                     # C
            'C' : {(0, 0)},                     # W
            'W' : {(0, 1), (0, 2)} }),          # W
                                                # ---------------------------
        'bucket' : Recipe( {                    # I   I
            'I' : {(0, 0), (1, 1), (2, 0)} }),  #   I
                                                # ---------------------------
        'axe' : Recipe( {                       # I W W
            'I' : {(0, 0)},                     #
            'W' : {(1, 0), (2, 0)} }),          #
                                                # ---------------------------
        'knife' : Recipe( {                     # I 
            'I' : {(0, 0)},                     # W
            'W' : {(0, 1)} }),                  #
                                                #
        # We can manage long sword              # 
        # due to sparse grid.                   #
        # If we use n*m matrix for              #
        # workbench grid / recipe storing       #
        # we will need minimum                  #
        # about 40 Gb of RAM to store it.       # ---------------------------
        'very_long_sword' : Recipe(             # W     (blade length = 10^5)
            generate_long_sword())              #   I 
    }                                           #     I
                                                #      ...
                                                #         I
