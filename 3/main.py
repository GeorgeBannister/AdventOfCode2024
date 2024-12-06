import re
from pathlib import Path

test_inp = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

test_inp_2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

inp = (Path(__file__).parent / 'inp.txt').read_text()

re_1 = re.compile(r'mul[(](-?\d+),(-?\d+)[)]')
do_re = re.compile(r'do[(][)]')
dont_re = re.compile(r"don't[(][)]")


def pt1(inp: str) -> int:
    acc = 0
    for match in re_1.finditer(inp):
        acc += int(match.group(1)) * int(match.group(2))
    return acc


def pt2(inp: str) -> int:
    do_idxs = [match.end(0) for match in do_re.finditer(inp)]
    dont_idxs = [match.end(0) for match in dont_re.finditer(inp)]
    acc = 0
    for match in re_1.finditer(inp):
        if max((x for x in do_idxs if x <= match.start(0)), default=0) > max(
            (x for x in dont_idxs if x <= match.start(0)),
            default=-1,
        ):
            acc += int(match.group(1)) * int(match.group(2))
    return acc


assert pt1(test_inp) == 161
print(f'{pt1(inp) = }')
assert pt2(test_inp_2) == 48
print(f'{pt2(inp) = }')
