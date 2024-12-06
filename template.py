from pathlib import Path

test_inp = """\
"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


def pt1(inp: str) -> int:
    return 0


def pt2(inp: str) -> int:
    return 0


assert pt1(test_inp) == 0
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 0
print(f'{pt2(inp) = }')
