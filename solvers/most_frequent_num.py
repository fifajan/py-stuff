#! /usr/bin/python

def most_popular_number(arr, n):
    """Return minimal most fruequent number in list."""
    if len(arr) != n:
        raise Exception('Bad input.')

    num_count = dict()
    for n in arr:
        num_count[n] = num_count.get(n, 0) + 1

    most_frequent = max(num_count, key=num_count.get)
    val = num_count[most_frequent]

    return min(n for n in num_count if num_count[n] == val)

if __name__ == '__main__':
    # Test cases:
    assert most_popular_number([34, 31, 34, 77, 82], 5) == 34
    assert most_popular_number([22, 101, 102, 101, 102, 525, 88], 7) == 101
    assert most_popular_number([66], 1) == 66
