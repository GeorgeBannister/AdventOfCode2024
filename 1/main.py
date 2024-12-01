from pathlib import Path

test_inp = """\
3   4
4   3
2   5
1   3
3   9
3   3"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


def pt1(inp: str) -> int:
    ls = []
    rs = []
    for line in inp.splitlines():
        lhs, rhs = line.split()
        ls.append(int(lhs))
        rs.append(int(rhs))
    ls.sort()
    rs.sort()
    return sum(abs(a[0] - a[1]) for a in zip(ls, rs))


def pt2(inp: str) -> int:
    ls = []
    rs = []
    for line in inp.splitlines():
        lhs, rhs = line.split()
        ls.append(int(lhs))
        rs.append(int(rhs))
    acc = 0
    for x in ls:
        for y in rs:
            if x == y:
                acc += x
    return acc


assert pt1(test_inp) == 11
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 31
print(f'{pt2(inp) = }')
