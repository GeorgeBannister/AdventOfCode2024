from __future__ import annotations

import itertools
import re
from dataclasses import dataclass, replace
from pathlib import Path

test_inp = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


test_inp_2 = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

inp = (Path(__file__).parent / 'inp.txt').read_text()
nums_re = re.compile(r'\d+', re.MULTILINE)


class BadMachineException(Exception): ...


class BadMachineExceptionPrint(Exception): ...


@dataclass
class Machine:
    a: int
    b: int
    c: int
    ip: int = 0
    outl = None
    goal = None

    def bump_ip(self: Machine) -> None:
        self.ip += 2

    def combo(self: Machine, op: int) -> int:
        if op in range(4):
            return op
        if op == 4:
            return self.a
        if op == 5:
            return self.b
        if op == 6:
            return self.c
        raise RuntimeError

    def adv(self: Machine, op: int) -> None:
        self.a = self.a // pow(2, self.combo(op))
        self.bump_ip()

    def bxl(self: Machine, op: int) -> None:
        self.b = self.b ^ op
        self.bump_ip()

    def bst(self: Machine, op: int) -> None:
        self.b = self.combo(op) % 8
        self.bump_ip()

    def jnz(self: Machine, op: int) -> None:
        if self.a == 0:
            self.bump_ip()
            return
        self.ip = op

    def bxc(self: Machine, _: int) -> None:
        self.b = self.b ^ self.c
        self.bump_ip()

    def out(self: Machine, op: int) -> None:
        if self.outl is None:
            self.outl = []
        self.outl.append(self.combo(op) % 8)
        if not self.on_track():
            if len(self.outl) > 15:
                raise BadMachineExceptionPrint
            raise BadMachineException
        self.bump_ip()

    def bdv(self: Machine, op: int) -> None:
        self.b = self.a // pow(2, self.combo(op))
        self.bump_ip()

    def cdv(self: Machine, op: int) -> None:
        self.c = self.a // pow(2, self.combo(op))
        self.bump_ip()

    def consume(self: Machine, ins: list[int]) -> bool:
        if self.ip + 1 > len(ins):
            return False

        match ins[self.ip]:
            case 0:
                self.adv(ins[self.ip + 1])
            case 1:
                self.bxl(ins[self.ip + 1])
            case 2:
                self.bst(ins[self.ip + 1])
            case 3:
                self.jnz(ins[self.ip + 1])
            case 4:
                self.bxc(ins[self.ip + 1])
            case 5:
                self.out(ins[self.ip + 1])
            case 6:
                self.bdv(ins[self.ip + 1])
            case 7:
                self.cdv(ins[self.ip + 1])
            case _:
                raise RuntimeError
        return True

    def __str__(self: Machine) -> str:
        if not self.outl:
            return ''

        return ','.join([str(x) for x in self.outl])

    def on_track(self: Machine) -> bool:
        if not self.goal:
            return True

        if len(self.outl) > len(self.goal):
            return False

        return not any(a != b for a, b in zip(self.outl, self.goal, strict=False))


def parse_inp(inp: str) -> tuple[Machine, list[int]]:
    nums = [int(x) for x in nums_re.findall(inp)]
    return Machine(*nums[:3]), nums[3:]


def pt1(inp: str) -> str:
    machine, ins = parse_inp(inp)
    cont = True
    while cont:
        cont = machine.consume(ins)
    return str(machine)


def pt2(inp: str) -> int:
    acc = 2977963573481

    machine_base, ins = parse_inp(inp)
    comp = ','.join(str(x) for x in ins)

    nums = []

    it = itertools.cycle((4, 1, 1, 16378, 4, 1, 1, 3431, 1099511607955))

    while len(nums) < 15:
        machine = replace(machine_base)
        machine.a = acc
        machine.goal = ins
        cont = True
        try:
            while cont:
                cont = machine.consume(ins)
                if str(machine) == comp:
                    return acc
        except BadMachineException:
            ...
        except BadMachineExceptionPrint:
            nums.append(acc)
            print(acc)
        acc += next(it)

    print(f'{nums = }')
    print('First diffs')
    fds = [b - a for a, b in itertools.pairwise(nums)]
    print(f'{fds = }')

    return acc


assert pt1(test_inp) == '4,6,3,5,6,3,5,2,1,0'
print(f'{pt1(inp) = }')
# assert pt2(test_inp_2) == 117440
# print('a2')
print(f'{pt2(inp) = }')
