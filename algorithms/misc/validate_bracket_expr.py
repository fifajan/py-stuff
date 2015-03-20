#! /usr/bin/python

def is_valid(expr):
    brackets = { ')' : '(', '}' : '{', ']' : '[' }
    stack = []
    for c in expr:
        if c in brackets.values():
            stack.append(c)
        elif c in brackets:
            if stack and stack[-1] == brackets[c]: stack.pop()
            else: return False

    return len(stack) == 0

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert is_valid("((5+3)*2+1)") == True, "Simple"
    assert is_valid("{[(3+1)+2]+}") == True, "Different types"
    assert is_valid("(3+{1-1)}") == False, ") is alone inside {}"
    assert is_valid("[1+1]+(2*2)-{3/3}") == True, "Different operators"
    assert is_valid("(({[(((1)-2)+3)-3]/3}-3)") == False, "One is redundant"
