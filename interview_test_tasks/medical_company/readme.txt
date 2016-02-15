Hello!

This README document describes all necessary details about
my implementation of test assessment task generously provided by M Company.

Programs were written and tested in following environment:
- Ubuntu 12.04 GNU/Linux OS on x86_64 architecture machine;
- Python 2.7.3
(I am pretty sure it should work in your environment if it differs
but if some mysterious problems will happen try to test in a similar env.)


Files:
 alexey_ivchenko_msc_task (root directory):
   - workbench.py: #1 task implemetation;
   - wb_test.py (executable): unit-tests for #1 task,
               Tests shoud run if executed in terminal;
   - call_args.py (executable): #2 task implementation,
               Tests shoud run if executed in terminal;
   - integer_field.py (executable): #3 task implementation;
               Tests shoud run if executed in terminal;
   - task.pdf: initial task sent to me by X (MC);
   - readme.txt: this document;
   - git_log.txt (optional): entire git repo log for this project.

   (Implementation details, design decisions etc could be found in comments
   inside those listed source files.)


Workbench usage example (see more in wb_test.py):

$ cd <path>/alexey_ivchenko_msc_task
$ python

>>> from workbench import Workbench, Recipe, CorrectRecipes
>>> w = Workbench() # create workbench
>>> r = Recipe( { 'I' : {(0, 0)}, 'W' : {(0, 1)} } ) # create 'knife' recipe
>>> w.add_recipe_items(r)
>>> w.craft() # try to craft something
'knife' # knife was crafted successfully
>>> w.clear() # clear workbench
>>> w.add_item('I', (0, 0)) # add single item to workbench
>>> w.add_item('I', (1, 1))
>>> w.add_item('I', (2, 0))
>>> w.craft() # try to craft something
'bucket' # bucket was crafted successfully
>>> w.celar()
>>> long_sword_r = CorrectRecipes.recipes['very_long_sword']
>>> w.add_recipe_items(long_sword_r)
>>> w.craft('very_long_sword') # try to craft something specific
'very_long_sword' # sword (length = 10^5) was crafted successfully
>>> w.clear()
>>> w.add_item('X', (10**18, 10**19)) # large indices are supported 
>>> w.craft() # try to craft something
>>>           # None returnde. It means that craft failed to craft anything
# see help:
>>> help(Workbench)
>>> help(Recipe)
>>> help(CorrectRecipes)
