FONT = ("--X--XXX-XXX-X-X-XXX--XX-XXX-XXX--XX-XX--",
        "-XX----X---X-X-X-X---X-----X-X-X-X-X-X-X-",
        "--X---XX--X--XXX-XX--XXX--X--XXX-XXX-X-X-",
        "--X--X-----X---X---X-X-X-X---X-X---X-X-X-",
        "--X--XXX-XXX---X-XX---XX-X---XXX-XX---XX-")

DIGITS_PIX_W_RES = 3
DIGITS_PIX_H_RES = 5
DIGITS_N = 10
FONT_PIX_LEN = DIGITS_PIX_W_RES * DIGITS_N


def is_equal_with_n_pix_error(d_1, d_2, pix_err_n=1):
    err_list = [x != d_2[i] for i, x in enumerate(d_1)]
    return sum(err_list) <= pix_err_n

def spaces_removed(img_list):
    return [x for i, x in enumerate(img_list) if i % (DIGITS_PIX_W_RES + 1)]

def digit(n, img_list, img_len=FONT_PIX_LEN):
    n = n - 1 if n else 9
    return [x for i, x in enumerate(img_list) if (
                DIGITS_PIX_W_RES * n <= i - (i // img_len) * img_len < (
                                DIGITS_PIX_W_RES * (n + 1)))]

def read_number(image):
    # convert both font and image to 1-d 0/1 int list
    font = [int(y) for x in FONT for y in (
                                x[:-1].replace('X', '1').replace('-', '0'))]
    image = [y for x in image for y in x[:-1]]

    font = spaces_removed(font)
    image = spaces_removed(image)

    image_pix_len = len(image) // DIGITS_PIX_H_RES
    image_dig_len = image_pix_len // DIGITS_PIX_W_RES

    res = ''
    for img_i in range(1, image_dig_len + 1):
        for font_i in range(DIGITS_N):
            if is_equal_with_n_pix_error(
                    digit(img_i, image, image_pix_len), digit(font_i, font)):
                res += str(font_i)
                break

    return int(res)

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert read_number([[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
                        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                        [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]]) == 394, (
                                                                "394 clear")
    assert read_number([[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
                        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
                        [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]]) == 394, (
                                                  "again 394 but with noise")
