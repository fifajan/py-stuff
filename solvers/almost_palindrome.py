#! /usr/bin/python

def is_almost_palindrome(word):
    """Checks if string is an 'almost' (1 character miss) palindrome."""
    mid = len(word) / 2
    l, r = word[:mid], word[mid:]
    r = r[::-1] # reverse
    if l == r:
        return True
    else: # not a true palindrome
        diff = 0
        for i in range(mid):
            diff += l[i] != r[i]
            if diff > 1:
                return False

        return diff == 1


if __name__ == '__main__':
    # Test cases:
    assert is_almost_palindrome('abccba')
    assert is_almost_palindrome('abccbx')
    assert is_almost_palindrome('abccbx')
    assert is_almost_palindrome('hello12olleh')
    assert not is_almost_palindrome('hxllo12olleh')
    assert not is_almost_palindrome('ayccbx')

