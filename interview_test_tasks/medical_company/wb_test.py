#! /usr/bin/python

# (c) Alexey Ivchenko (yanepman@gmail.com), 2015

# Those tests provide 100% coverage of workbench.py
# You can check it yourself by using 'coverage.py' tool:
#  $ coverage run wb_test.py
#  $ coverage html workbench.py
#    HTML results will be in 'htmlcov' directory.

import unittest

from workbench import Recipe, Workbench, CorrectRecipes

class TestTaskExamples(unittest.TestCase):
    """Test workbench with exact examples provided in PDF."""

    def test_successful(self):
        # Torch crafting:
        w = Workbench()
        r = Recipe({'C' : {(2, 0)}, 'W' : {(2, 1), (2, 2)}})
        w.add_recipe_items(r)
        self.assertEqual('torch', w.craft())

        w.clear()
        r = Recipe({'C' : {(3, 1)}, 'W' : {(3, 2), (3, 3)}})
        w.add_recipe_items(r)
        self.assertEqual('torch', w.craft())

        w.clear()
        r = Recipe({'C' : {(0, 0)}, 'W' : {(0, 1), (0, 2)}})
        w.add_recipe_items(r)
        self.assertEqual('torch', w.craft())

        # Bucket crafting:
        w.clear()
        r = Recipe({'I' : {(0, 1), (1, 2), (2, 1)}})
        w.add_recipe_items(r)
        self.assertEqual('bucket', w.craft())

        w.clear()
        r = Recipe({'I' : {(2, 0), (3, 1), (4, 0)}})
        w.add_recipe_items(r)
        self.assertEqual('bucket', w.craft())

    def test_fail(self):
        # Torch crafting:
        w = Workbench()
        r = Recipe({'C' : {(2, 2)}, 'W' : {(2, 0), (2, 1)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'C' : {(0, 2)}, 'W' : {(0, 0), (0, 3)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'C' : {(1, 0)}, 'W' : {(1, 2), (1, 3)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'C' : {(1, 0)}, 'W' : {(1, 1), (1, 2), (1, 3)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'C' : {(1, 0)}, 'W' : {(2, 0), (3, 0)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'C' : {(1, 0)}, 'W' : {(3, 1), (1, 2), (1, 3)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'C' : {(1, 1), (2, 1)},
                    'W' : {(1, 2), (2, 2), (1, 3), (2, 3)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        # Bucket crafting:
        w.clear()
        r = Recipe({'I' : {(0, 1), (1, 2), (2, 1), (3, 0)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'I' : {(0, 1), (1, 2), (3, 0)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'I' : {(0, 1), (1, 1), (2, 1)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

        w.clear()
        r = Recipe({'I' : {(0, 1), (1, 2), (2, 1)}, 'W' : {(4, 2)}})
        w.add_recipe_items(r)
        self.assertEqual(None, w.craft())

class TestRecipe(unittest.TestCase):
    def test_successful(self):
        # offsets from (0, 0) origin
        r = Recipe({'I' : {(2, 3)}, 'W' : {(2, 4)}})
        r.optimize_position()
        self.assertEqual('knife', r.get_name())

        # large offsets from (0, 0) origin
        r = Recipe({'I' : {(10**15 + 2, 10**14 + 3),
                           (10**15 + 3, 10**14 + 4),
                           (10**15 + 4, 10**14 + 3)}})
        r.optimize_position()
        self.assertEqual('bucket', r.get_name())
        # test cache
        self.assertEqual('bucket', r.get_name())

    def test_fail(self):
        r = Recipe({'X' : {(10, 11)}})
        r.optimize_position()
        self.assertEqual(None, r.get_name())

        # invalid positions
        r = Recipe({'X' : {((1, 3, 5), 'hello')}})
        with self.assertRaises(IndexError):
            r.optimize_position()

class TestCrafting(unittest.TestCase):
    def test_successful(self):
        w = Workbench()

        recipes = CorrectRecipes.recipes

        for name, recipe in recipes.items():
            w.add_recipe_items(recipe)
            self.assertEqual(name, w.craft())
            w.clear()

        w.add_recipe_items(recipes['axe'])
        self.assertEqual('axe', w.craft())

        w.clear()
        w.add_recipe_items(recipes['very_long_sword'])
        self.assertEqual('very_long_sword', w.craft('very_long_sword'))

    def test_fail(self):
        w = Workbench()

        w.add_item('O', (5, 6))
        self.assertEqual(None, w.craft())
        self.assertEqual(None, w.craft('knife'))

        with self.assertRaises(KeyError):
            w.craft('space_ship')


class TestItemsPrinting(unittest.TestCase):
    def test_print(self):
        w = Workbench()

        self.assertEqual(str(w), ('++\n'
                                  '||\n'
                                  '++'))

        w.add_item('A', (0, 0))
        self.assertEqual(str(w), ('+-+\n'
                                  '|A|\n'
                                  '+-+'))
        w.add_item('A', (2, 2))
        self.assertEqual(str(w), ('+---+\n'
                                  '|A  |\n'
                                  '|   |\n'
                                  '|  A|\n'
                                  '+---+'))
        w.add_item('B', (1, 1))
        self.assertEqual(str(w), ('+---+\n'
                                  '|A  |\n'
                                  '| B |\n'
                                  '|  A|\n'
                                  '+---+'))

        w.add_item('C', (10, 5))
        self.assertEqual(str(w), ('+-----------+\n'
                                  '|A          |\n'
                                  '| B         |\n'
                                  '|  A        |\n'
                                  '|           |\n'
                                  '|           |\n'
                                  '|          C|\n'
                                  '+-----------+'))

        w.add_item('D', (10**15, 10**17))
        self.assertEqual(str(w), 'Workbench is too big to print it!')


class TestItemsAdditionAndCount(unittest.TestCase):
    def test_add_item_count(self):
        w = Workbench()
        self.assertEqual(len(w), 0)

        w.add_item('X', (5, 5))
        self.assertEqual(len(w), 1)

        w.add_item('Y', (5, 5))
        self.assertEqual(len(w), 1)

        w.add_item('Z', (0, 0))
        self.assertEqual(len(w), 2)

        w.add_item('A', (-100, -500))
        self.assertEqual(len(w), 3)

        w.clear()
        self.assertEqual(len(w), 0)

    def test_large_indices(self):
        w = Workbench()

        w.add_item('X', (10**3, 10**3))
        w.add_item('Y', (10**6, 10**6))
        w.add_item('Z', (10**20, 10**20))

        self.assertEqual(len(w), 3)

    def test_invalid_positions(self):
        w = Workbench()

        with self.assertRaises(IndexError):
            w.add_item('X', ('hello', 5))
        with self.assertRaises(IndexError):
            w.add_item('X', (10, 'world'))
        with self.assertRaises(IndexError):
            w.add_item('X', (['a'], (12,)))

if __name__ == '__main__':
    unittest.main()
