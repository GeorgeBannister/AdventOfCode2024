from pathlib import Path

test_inp = """\
1
10
100
2024"""

test_inp_2 = """\
1
2
3
2024"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


type DeltaSequence = tuple[int, int, int, int]


def last_digit(inp: int) -> int:
    return int(str(inp)[-1])


def is_valid_sequence_with_start(r: DeltaSequence, start: int) -> bool:
    for d in r:
        start += d
        if not (-10 < start < 10):
            return False
    return True


def is_valid_sequence(r: DeltaSequence) -> bool:
    return any(is_valid_sequence_with_start(r, x) for x in range(-9, 10))


def iteration(secret: int) -> int:
    tmp = secret << 6
    secret = (tmp ^ secret) % 16777216
    tmp = secret >> 5
    secret = (tmp ^ secret) % 16777216
    tmp = secret << 11
    return (tmp ^ secret) % 16777216


def do_iters(inp: int, iters: int) -> int:
    for _ in range(iters):
        inp = iteration(inp)
    return inp


def pt1(inp: str) -> int:
    return sum(do_iters(int(x), 2000) for x in inp.splitlines())


def pt2_helper(init_magic: int) -> list[tuple[tuple[int], int]]:
    last_4_deltas = [None, None, None, None]
    last_last_digit = last_digit(init_magic)
    acc = {}
    for _ in range(2000):
        init_magic = iteration(init_magic)
        tmp = last_digit(init_magic)
        last_4_deltas[0] = last_4_deltas[1]
        last_4_deltas[1] = last_4_deltas[2]
        last_4_deltas[2] = last_4_deltas[3]
        last_4_deltas[3] = tmp - last_last_digit
        last_last_digit = tmp
        ld = tuple(last_4_deltas)
        if ld not in acc:
            acc[ld] = last_last_digit
    return acc


def pt2(inp: str) -> int:
    acc = []
    inits = [int(line) for line in inp.splitlines()]
    bla = [pt2_helper(init) for init in inits]
    for a in range(-9, 10):
        for b in range(-9, 10):
            for c in range(-9, 10):
                for d in range(-9, 10):
                    delta_s = (a, b, c, d)
                    if is_valid_sequence(delta_s):
                        acc_2 = 0
                        for poggy in bla:
                            acc_2 += poggy.get(delta_s, 0)
                        acc.append((delta_s, acc_2))
    return max(x[1] for x in acc)


assert pt1(test_inp) == 37327623
print(f'{pt1(inp) = }')
assert pt2(test_inp_2) == 23
print(f'{pt2(inp) = }')
