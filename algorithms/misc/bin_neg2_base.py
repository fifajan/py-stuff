#! /usr/bin/python

'''
Tools for (-2) base binary system.
'''

def get_number_neg2(bits):
    return sum(b * ((-2)**i) for i, b in enumerate(bits))

def get_bits_neg2(number):
    result = []
    while number:
        remainder = number % -2
        number /= -2
        if remainder < 0:
            remainder += 2
            number += 1
        result.append(remainder)
    return result

if __name__ == '__main__':
    assert 5 == get_number_neg2([1, 0, 1])
    assert -111 == get_number_neg2([1, 0, 0, 0, 1, 0, 0, 1])
    assert [0, 1, 0, 0, 1] == get_bits_neg2(14)
