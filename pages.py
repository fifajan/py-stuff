#! /usr/bin/python3

'''Script for page numbers generation. Aim is to make printing brochures
"easy".'''


def pages(total, even_only=True):
    result = []
    for pages_4 in div_by_4(int(total)):
        p1, p2, p3, p4 = pages_4
        if even_only:
            brochured = [str(p) for p in [p4, p1]]
        else:
            brochured = [str(p) for p in [p2, p3]]
        result.extend(brochured)

    print(result)
    return ', '.join(result)

def div_by_4(total):
    result = []
    of_4 = 1
    pages_4 = []
    for page_num in range(1, total + 1):
        if of_4 > 4:
            of_4 = 1
            result.append(pages_4)
            pages_4 = []

        pages_4.append(page_num)
        of_4 += 1

    if len(pages_4) < 4:
        left = 4 - len(pages_4)
        pages_4 += [None] * left

    result.append(pages_4)

    return result


if __name__ == '__main__':
    from sys import argv

    if (len(argv) != 3) or not argv[1].isdigit():
        print('USAGE: $ ./pages.py <TOTAL_PAGE_COUNT>')
    else:
        even_only = False
        if argv[2].upper() == 'E':
            even_only = True

        print(pages(argv[1], even_only))
