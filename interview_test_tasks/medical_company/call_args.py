#! /usr/bin/python

# (c) Alexey Ivchenko (yanepman@gmail.com), 2015

from inspect import getargspec

def get_call_args(func, *args, **kwargs):
    arg_spec = getargspec(func).__getnewargs__()
    positional = arg_spec[0]
    defaults = list(arg_spec[-1])
    result = {}
    if args:
        args_left = []
        for a in args:
            if positional:
                name = positional.pop(0)
                result[name] = a
                if kwargs and name in kwargs:
                    result[name] = kwargs[name]
                    del kwargs[name]
            else:
                args_left.append(a)
        for a in positional:
            result[a] = kwargs[a] if a in kwargs else defaults.pop(0)
            if a in kwargs:
                del kwargs[a]
        if 'args' in arg_spec:
            result['args'] = tuple(args_left)
    if kwargs:
        result['kwargs'] = kwargs
    return result

if __name__ == '__main__':

    # Test input functions:
    def cool_func(a, b, c=10, d=20, *args, **kwargs):
        return locals()

    def my_func(x, y, z=(1, 2, ['hello', 'world']), *args):
        return locals()

    def my_another_func(p1, p2, p3={(1, 2), '3', 4}, **kwargs):
        return locals()

    # Tests:
    local_vars = cool_func(1, 2, 3, 4, 5, 6, 7, 8, 9, x=100, y=200, z=300)
    assert get_call_args(cool_func,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, x=100, y=200, z=300) == (
                local_vars ) == {  # correct (copied from PDF) ->
                        'a': 1, 'b': 2, 'c': 3, 'd': 4,
                        'args': (5, 6, 7, 8, 9),
                        'kwargs': {'y': 200, 'x': 100, 'z': 300} }


    local_vars = cool_func(1, 2, d=100, y=200, z=300)
    assert get_call_args(cool_func, 1, 2, d=100, y=200, z=300) == (
                local_vars ) == {  # correct (copied from PDF) ->
                'a': 1, 'b': 2, 'c': 10, 'd': 100,
                'args': (), 'kwargs': {'y': 200, 'z': 300} }


    local_vars = my_func(22, 33, 44, 55, 66)
    assert get_call_args(my_func, 22, 33, 44, 55, 66) == local_vars


    local_vars = my_func(11, 12)
    assert get_call_args(my_func, 11, 12) == local_vars


    local_vars = my_another_func(11, 12, 13, hello='world')
    assert get_call_args(my_another_func, 11, 12, 13, hello='world') == (
							local_vars )


    local_vars = my_another_func(-2, -3, hi='mom!')
    assert get_call_args(my_another_func, -2, -3, hi='mom!') == local_vars

    print 'Tests passed successfully!'
