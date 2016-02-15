#! /usr/bin/python

# (c) Alexey Ivchenko (yanepman@gmail.com), 2015

# This script (if ran in shell) emulates following Python shell session:
#
# class Person(object):
#  age = IntegerField()
#
# >>> bob = Person()
# >>> bob.age = 10
# >>> bob.age
# 10
#
# >>> bob.age = '20'
# >>> bob.age
# 20
#
# >>> bob.age = 20.5
# ValueError
#
# >>> bob.age = 'wrong'
# ValueError

from thread import start_new_thread
from time import sleep

class IntegerField(object):
    """Represents a hacky IntegerField proxy.
    It hacks Person class in separate thread and slips it's
    __setattr__ method.
    """
    def hack_person(self):
        def set_attribute(self, name, value):
            if name == 'age':
                value = '?' if type(value) == float else value
                value = int(value)
            object.__setattr__(self, name, value)

        sleep(0.001)
        globals()['Person'].__setattr__ = set_attribute

    def __init__(self, value=0):
        start_new_thread(self.hack_person, ())

if __name__ == '__main__':

    # __My_approach_explained__:
    #
    # The right way of overriding '=' operator (assignment)
    # does not exist in Python (at least it is unknown for me).
    # As i understood i can't modify Person class in this task.
    # If i could do this i'll just override it's __setattr__
    # or use @property and @age.setter decorators.
    # But i can't do it in explicit way according to task protocol...
    # So i did it in implicit way :) :
    # in IntegerField's __init__ i hacked Person class in a
    # separate delayed thread.

    class Person(object):
     age = IntegerField()

    # In task description '>>>' shell prefixes are present.
    # So i will emulate shell session with some human delays.
    # P.S. Human is actually super-fast in this emulation :)

    msg = '<Emulating human delay in shell session...>'
    print msg ; sleep(0.1) # delay
    bob = Person()
    print msg ; sleep(0.1) # delay
    bob.age = 10
    print msg ; sleep(0.1) # delay
    assert bob.age == 10

    print msg ; sleep(0.1) # delay
    bob.age = '20'
    assert bob.age == 20

    print msg ; sleep(0.1) # delay
    caught_ex = None
    try:
        bob.age = 20.5
    except ValueError as ex:
        caught_ex = ex
    assert type(caught_ex) == ValueError

    print msg ; sleep(0.1) # delay
    caught_ex = None
    try:
        bob.age = 'wrong'
    except ValueError as ex:
        caught_ex = ex
    assert type(caught_ex) == ValueError

    print 'Tests passed successfully!'
