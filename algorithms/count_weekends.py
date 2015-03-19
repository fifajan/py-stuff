#! /usr/bin/python

from datetime import date, timedelta

def count_we(from_date, to_date):
    return len([d for d in [from_date + timedelta(n) for n in range(
                    (to_date - from_date).days + 1)] if 4 < d.weekday() < 7])

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert count_we(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
    assert count_we(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
    assert count_we(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"

