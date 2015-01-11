from re import match, compile

N = 3
pattern = compile('^X{%d}|O{%d}$' % (N, N))

def game_lines(game_result):
    # add horizontal lines
    lines = game_result
    # add vertical lines
    lines += [''.join([line[i] for line in game_result]) for i in range(N)]
    # add diagonals
    lines += [''.join([game_result[i][i] for i in range(N)]),
                ''.join([game_result[-(i + 1)][i] for i in range(N)])]
    return lines

def x_o(game_result):
    for line in game_lines(game_result):
        if match(pattern, line): return line[0]
    else: return "D"

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert x_o([
        "X.O",
        "XX.",
        "XOO"]) == "X", "Xs wins"
    assert x_o([
        "OO.",
        "XOX",
        "XOX"]) == "O", "Os wins"
    assert x_o([
        "OOX",
        "XXO",
        "OXX"]) == "D", "Draw"
