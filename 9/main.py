import itertools
from pathlib import Path

test_inp = """\
2333133121414131402"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


type Filesystem = list[int | None]


def parse_inp(inp: str) -> Filesystem:
    inp = inp.strip()
    if len(inp) % 2 == 1:
        inp += '0'
    acc = []
    for idx, tup in enumerate(itertools.batched(inp, 2)):
        n_blocks, n_space = tup
        for _ in range(int(n_blocks)):
            acc.append(int(idx))
        for _ in range(int(n_space)):
            acc.append(None)
    return acc


def free_space_idx(fs: Filesystem) -> int:
    for idx, val in enumerate(fs):
        if val is None:
            return idx
    raise RuntimeError


def is_packed(fs: Filesystem) -> bool:
    none_found = False
    for val in fs:
        if val is None:
            none_found = True
        elif none_found:
            return False
    return True


def pt1(inp: str) -> int:
    fs = parse_inp(inp)

    while not is_packed(fs):
        for idx in range(len(fs) - 1, -1, -1):
            if fs[idx] is not None:
                free_idx = free_space_idx(fs)
                if free_idx > idx:
                    continue
                fs[free_idx] = fs[idx]
                fs[idx] = None

    acc = 0
    for idx, val in enumerate(fs):
        if val is not None:
            acc += idx * val
    return acc


def none_spans(fs: Filesystem):
    acc = []
    for idx, val in enumerate(fs):
        if val is None:
            acc.append(idx)
        elif acc:
            yield acc
            acc = []


def pt2(inp: str) -> int:
    fs = parse_inp(inp)
    max_f = max(x for x in fs if x)
    for curr_val in range(max_f, -1, -1):
        curr_val_idxs = [i for i, val in enumerate(fs) if val == curr_val]
        l = len(curr_val_idxs)
        span_found = False
        for span in none_spans(fs):
            if span[0] >= curr_val_idxs[0]:
                break
            if span_found:
                break
            if len(span) >= l:
                span_found = True
                for i in range(l):
                    fs[span[i]] = curr_val
                    fs[curr_val_idxs[i]] = None
    acc = 0
    for idx, val in enumerate(fs):
        if val is not None:
            acc += idx * val
    return acc


assert pt1(test_inp) == 1928
print('A1')
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 2858
print('A2')
print(f'{pt2(inp) = }')
