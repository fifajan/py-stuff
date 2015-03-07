#! /usr/bin/python

from sys import argv
import random as rand

def write_int_array_to_text_file(filename, lenght=100, do_stuffle=False):
    offset_range = range(-lenght, lenght + 1)
    offset = rand.choice(offset_range)

    abs_offset = abs(offset)
    half_abs_offset_range = range(abs_offset // 2)
    int_list = [_int + i*abs_offset + rand.choice(half_abs_offset_range) for (
                    i, _int) in enumerate(range(offset, lenght + offset))]
    if do_stuffle:
        rand.shuffle(int_list)

    with open(filename, 'w') as f:
        for i in int_list:
            f.write(str(i) + '\n')

if __name__ == '__main__':
    if len(argv) < 3:
        print ('USAGE: $ ./gen_int_arrays.py '
               '<N_FILES> <N_INTs_IN_FILE> [r] [<FILE_NAME>]')
    else:
        n_ints = int(argv[2])
        n_files = int(argv[1])
        shuffle = (argv[3].lower() == 'r') if len(argv) > 3 else False
        name_pattern = ('rand_' if shuffle else '') + 'ints_%05i.txt'
        filename = []
        if n_files == 1:
            # i know below isn't very straightforward but it still works:
            filename = (
                name_pattern % 0) if (((len(argv) < 5) and shuffle) or (
                                      ((len(argv) < 4) and not shuffle))) else (
                                            argv[4 if shuffle else 3])
        else:
            for i in range(n_files):
                name = name_pattern % i
                filename.append(name)

        if type(filename) is list:
            for f in filename:
                write_int_array_to_text_file(f, n_ints, shuffle)
        else:
            if filename:
                write_int_array_to_text_file(filename, n_ints, shuffle)
