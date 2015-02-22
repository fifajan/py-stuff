#! /usr/bin/python

K = 0
V = 1

class HashMap(object):
    '''
    My attempt to implement hash map (open addressing).
    Inspired by a wonderful article about dicts in Python (russian):
    http://habrahabr.ru/post/247843/
    It happen to be only 3.5 times slower than standart dict!
    (see some basic tests sources & timings in 'tests' sub dir).
    '''

    # Hash table size should be a prime. Few primes below 10^6 + 4
    table_size_primes = {
        (0, 11) : 11,
        (12, 101) : 101,
        (102, 1009) : 1009,
        (1010, 10**4 + 7) : 10007,
        (10**4 + 8, 10**5 + 3) : 100003,
        (10**5 + 4, 10**6 + 3) : 1000003,
    }

    probe_step = 3

    def __init__(self, *args, **kwargs):
        size = kwargs['size'] if 'size' in kwargs else 100
        self.size = 0
        self.collisions = 0
        self.table_size_range, self.table_size = self.get_prime_size(size)
        self.table = [None] * self.table_size 

        if args:
            for a in args:
                self.add(a)

    # PRIVATE -->

    def get_prime_size(self, size):
        for mn, mx in self.table_size_primes:
            if mn <= size <= mx:
                return (mn, mx), self.table_size_primes[(mn, mx)]
        return size

    def hash(self, key): # using just a standart library hashing here
        h = hash(key)
        return h % self.table_size

    def has_hash(self, h):
        return self.table[h] is not None

    def __repr__(self):
        res = '{'
        i = 0
        for k_v in self.table:
            if k_v:
                if i:
                    res += ', '
                res += '%s: %s' % tuple(map(repr, k_v))
                i += 1
        return res + '}'

    def __iter__(self):
        return [k_v[K] for k_v in self.table if k_v is not None].__iter__()

    # PUBLIC -->

    def remove(self, key):
        h = self.hash(key)
        if self.has_key(key):
            while key != self.table[h][K]:
                h += self.probe_step
                h %= self.table_size
            self.table[h] = None
            self.size -= 1
        else:
            raise KeyError, "No such key (can't remove)"

    def add(self, (key, val)):
        h = self.hash(key)
        if not self.has_key(key):
            self.table[h] = [key, val]
            self.size += 1
            # it is good for hash table to be 1/3 empty
            # if self.table_size - self.size < self.table_size / 3.0:
            #     new_table_size = self.get_prime_size(
            #                         self.table_size_range[1] + 1)
            # TODO: finish auto-extension of hash table

        elif key != self.table[h][K]:
            while self.has_hash(h):
                h += self.probe_step
                h %= self.table_size
                self.collisions += 1
            self.table[h] = [key, val]
        elif val != self.table[h][V]:
            self.table[h][V] = val

    def has_key(self, key):
        for k_v in self.table:
            if k_v and key == k_v[K]:
                return True 
        return False
        
    def get(self, key):
        h = self.hash(key)
        if self.has_key(key):
            while self.table[h][K] != key:
                h += self.probe_step
                h %= self.table_size
            return self.table[h][V]
        else:
            raise KeyError, 'No such key'

    def keys(self):
        return [k_v[K] for k_v in self.table if k_v is not None]

    def values(self):
        return [k_v[V] for k_v in self.table if k_v is not None]

    def items(self):
        return [k_v for k_v in self.table if k_v is not None]
