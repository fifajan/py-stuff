#! /usr/bin/python3

'''Script for page numbers generation. Aim is to make printing brochures
"easy".'''

def pages(total):
    return div_by_4(int(total))

def div_by_4(total):
    result = []
    of_4 = 1
    pages_4 = []
    for page_num in range(total):
        if of_4 > 4:
            pages_4 = []
            of_4 = 1
            result.append(pages_4)

        pages_4.append(page_num)
        of_4 += 1

    return result


if __name__ == '__main__':
    from sys import argv

    if (len(argv) != 2) or not argv[1].isdigit():
        print('USAGE: $ ./pages.py <TOTAL_PAGE_COUNT>')
    else:
        print(pages(argv[1]))
