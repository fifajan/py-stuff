#! /usr/bin/python

def is_perfect_number(num):
    divisors = [i for i in range(1, num) if num % i == 0]
    return num == sum(divisors)


if __name__ == '__main__':
    # Test cases:
    assert is_perfect_number(6)
    assert is_perfect_number(496)
    assert is_perfect_number(8128)
    assert not is_perfect_number(1234567)
