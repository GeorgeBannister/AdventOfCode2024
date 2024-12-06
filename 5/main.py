from pathlib import Path

test_inp = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

inp = (Path(__file__).parent / 'inp.txt').read_text()

type Update = list[int]
type Presidence = tuple[int, int]


def parse_inp(inp: str) -> tuple[list[Presidence], list[Update]]:
    presidences = []
    updates = []
    for line in inp.splitlines():
        if '|' in line:
            l, r = line.split('|')
            presidences.append((int(l), int(r)))
        if ',' in line:
            updates.append([int(x) for x in line.split(',')])
    return (presidences, updates)


def update_is_valid(update: Update, presidences: list[Presidence]) -> bool:
    for idx, num in enumerate(update):
        for pres in presidences:
            if pres[1] == num and pres[0] not in update[0:idx] and pres[0] in update[idx:]:
                return False
    return True


def pt1(inp: str) -> int:
    presidences, updates = parse_inp(inp)
    acc = 0
    for update in updates:
        if update_is_valid(update, presidences):
            acc += update[len(update) // 2]
    return acc


def reorder_update(update: Update, presidences: list[Presidence]) -> int:
    def swap_elems(l: Update, i: int, j: int) -> None:
        i1 = l.index(i)
        i2 = l.index(j)
        tmp = l[i1]
        l[i1] = l[i2]
        l[i2] = tmp

    did_change = True
    while did_change:
        did_change = False
        for idx, num in enumerate(update):
            for pres in presidences:
                if pres[1] == num and pres[0] not in update[0:idx] and pres[0] in update[idx:]:
                    swap_elems(update, pres[0], pres[1])
                    did_change = True
    return update[len(update) // 2]


def pt2(inp: str) -> int:
    presidences, updates = parse_inp(inp)
    acc = 0
    for update in updates:
        if not update_is_valid(update, presidences):
            acc += reorder_update(update, presidences)
    return acc


assert pt1(test_inp) == 143
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 123
print(f'{pt2(inp) = }')
