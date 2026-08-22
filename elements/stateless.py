from enum import Enum
from itertools import product

from . import common as C

ONE_PORT = [
    (C.Vals.L, ), # 0b0
    (C.Vals.H, ), # 0b1
]

TWO_PORT = [
    (C.Vals.L, C.Vals.L), # 0b00
    (C.Vals.H, C.Vals.L), # 0b01
    (C.Vals.L, C.Vals.H), # 0b10
    (C.Vals.H, C.Vals.H), # 0b11
]

THREE_PORT = [
    (C.Vals.L, C.Vals.L, C.Vals.L), # 0b000
    (C.Vals.H, C.Vals.L, C.Vals.L), # 0b001
    (C.Vals.L, C.Vals.H, C.Vals.L), # 0b010
    (C.Vals.H, C.Vals.H, C.Vals.L), # 0b011
    (C.Vals.L, C.Vals.L, C.Vals.H), # 0b100
    (C.Vals.H, C.Vals.L, C.Vals.H), # 0b101
    (C.Vals.L, C.Vals.H, C.Vals.H), # 0b110
    (C.Vals.H, C.Vals.H, C.Vals.H), # 0b111
]

FOUR_PORT = [
    (C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L), # 0b0000
    (C.Vals.H, C.Vals.L, C.Vals.L, C.Vals.L), # 0b0001
    (C.Vals.L, C.Vals.H, C.Vals.L, C.Vals.L), # 0b0010
    (C.Vals.H, C.Vals.H, C.Vals.L, C.Vals.L), # 0b0011
    (C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.L), # 0b0100
    (C.Vals.H, C.Vals.L, C.Vals.H, C.Vals.L), # 0b0101
    (C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.L), # 0b0110
    (C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.L), # 0b0111
    (C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H), # 0b1000
    (C.Vals.H, C.Vals.L, C.Vals.L, C.Vals.H), # 0b1001
    (C.Vals.L, C.Vals.H, C.Vals.L, C.Vals.H), # 0b1010
    (C.Vals.H, C.Vals.H, C.Vals.L, C.Vals.H), # 0b1011
    (C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.H), # 0b1100
    (C.Vals.H, C.Vals.L, C.Vals.H, C.Vals.H), # 0b1101
    (C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.H), # 0b1110
    (C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H), # 0b1111
]

def get_io():

    with open("cell-to-pins.txt") as fp:
        data = fp.read()

    ret = {}
    lines = data.splitlines()[2:]
    for line in lines:
        port, ins, outs = line.split("|")
        port = port.strip().replace('sky130_fd_sc_hd__','').replace("_1","").replace("_2","")
        ins = ins.strip().split(',')
        outs = outs.strip().split(',')
        ret[port] = (set(ins), set(outs))

    return ret
IO_PORTS=get_io()

def compare_io(obj):

    ins = set(obj.map[0].keys())
    cmp_ins = set(IO_PORTS[obj._type.lower()][0])
    assert ins == cmp_ins, f"Inputs {ins=} != {cmp_ins=}"

    outs = set(obj.map[1].keys())
    cmp_outs = set(IO_PORTS[obj._type.lower()][1])
    assert outs == cmp_outs, f"Outputs {outs=} != {cmp_outs=}"



class O21bai(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=3, nouts=1)
        self._type = "O21bai"
        self.map = {"A1": 0, "A2": 1, "B1_N": 2}, {"Y": 0}

    def tick(self, _, ins):
        assert len(ins) == 3
        _,_, _or = Or2().tick(None, ins[:2])
        _,_, _not = Not().tick(None, ins[2:])
        _,_,_and = And2().tick(None, _or + _not)
        _,_, _not1 = Not().tick(None, _and)

        return None, None, _not1


def test_o21bai():

    compare_io(O21bai())

    for x,y,z in product(C.Vals, C.Vals, C.Vals):
        _, _, ret = O21bai().tick(None, [x,y,z])

        if C.Vals.Q in [x,y,z]:
            assert ret == [C.Vals.Q]
        elif z == C.Vals.H:
            assert ret == [C.Vals.H]
        else:
            _,_, _or = Or2().tick(None, [x,y])
            _,_, _not = Not().tick(None,_or)
            assert ret == _not

"""
No tests above this line ;(
class O21bai(C.Common):

"""


class A31o(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=4, nouts=1)
        self._type = "A31o"
        self.map = {"A1": 0, "A2": 1, "A3": 2, "B1": 3}, {"X": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        assert len(ins) == 4

        _,_,_and1 = And2().tick(None, [ins[0], ins[2]])
        _,_,_and2 = And2().tick(None, [ins[1]] + _and1)
        _,_,_or   = Or2().tick(None, [ins[3]] + _and2)

        return None, None, _or

def test_a32o():

    compare_io(A31o())
    for x,y,z,a in product(C.Vals, C.Vals, C.Vals, C.Vals):
        _, _, ret = A31o().tick(None, [x,y,z,a])

        if C.Vals.Q in [x,y,z,a]:
            assert ret == [C.Vals.Q]
        elif a == C.Vals.H:
            assert ret == [C.Vals.H]
        else:
            _,_, _and = And3().tick(None, [x,y,z])
            assert _and == ret

class And4bb(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=4, nouts=1)
        self._type = "And3"
        self.map = {"A_N": 0, "B_N": 1, "C": 2, "D": 3}, {"X": 0}
        self.pattern = [
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H,
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L,
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L,
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L,
        ]
        self.table = THREE_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

class And3(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=3, nouts=1)
        self._type = "And3"
        self.map = {"A": 0, "B": 1, "C": 2}, {"X": 0}
        self.pattern = [
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L,
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H,
        ]
        self.table = THREE_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

class A21o(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=3, nouts=1)
        self._type = "A21o"
        self.map = {"A1": 0, "A2": 1, "B1": 2}, {"X": 0}
        self.pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H]
        self.table = THREE_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        assert len(ins) == 3

        _, _, _as = And2().tick(None, ins[:2])
        _, _, _or = Or2().tick(None, _as + ins[2:])

        return None, None, _or

def test_a210():
    compare_io(A21o())
    for x,y,z in product(C.Vals, C.Vals, C.Vals):
        _, _, ret = A21o().tick(None, [x,y,z])

        if C.Vals.Q in [x,y,z]:
            assert ret == [C.Vals.Q]
        elif z == C.Vals.H:
            assert ret == [C.Vals.H]
        else:
            _,_, _and = And2().tick(None, [x,y])
            assert _and == ret

class A21boi(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=3, nouts=1)
        self._type = "A21boi"
        self.map = {"A1": 0, "A2": 1, "B1_N": 2}, {"Y": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        assert len(ins) == 3
        _, _, _as     = And2().tick(None, ins[:2])
        _, _, _not_b  = Not().tick(None, ins[2:])
        _, _, _or     = Or2().tick(None, _as + _not_b)
        _, _, ret     = Not().tick(None, _or)
        return None, None, ret

def test_a21boi():
    compare_io(A21boi())
    for x,y,z in product(C.Vals, C.Vals, C.Vals):
        _, _, ret = A21boi().tick(None, [x,y,z])

        if C.Vals.Q in [x,y,z]:
            assert ret == [C.Vals.Q]
        elif z == C.Vals.L:
            assert ret == [C.Vals.L]
        else:
            _,_, ret1 = And2().tick(None, [x,y])
            _,_, ret2 = Not().tick(None, ret1)
            assert ret == ret2, f"{x=} {y=}, {ret1=}, {ret2=}"

class A21bo(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=3, nouts=1)
        self._type = "A21bo"
        self.map = {"A1": 0, "A2": 1, "B1_N": 2}, {"X": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        assert len(ins) == 3
        _, _, _as     = And2().tick(None, ins[:2])
        _, _, _not_as = Not().tick(None, _as)
        _, _, _b_and  = And2().tick(None, _not_as + ins[2:])
        _, _, ret     = Not().tick(None, _b_and)
        return None, None, ret

def test_a21bo():
    compare_io(A21bo())
    for x,y,z in product(C.Vals, C.Vals, C.Vals):
        _, _, ret = A21bo().tick(None, [x,y,z])

        if C.Vals.Q in [x,y,z]:
            assert ret == [C.Vals.Q]
        elif z == C.Vals.L:
            assert ret == [C.Vals.H]
        else:
            _,_, ret1 = And2().tick(None, [x,y])
            assert ret == ret1, f"{x=} {y=}"

class Xnor2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=2, nouts=1)
        self._type = "Xnor2"
        self.map = {"A": 0, "B": 1}, {"Y": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        _, _, _xor = Xor2().tick(None, ins)
        _,_, _not = Not().tick(None, _xor)
        return None, None, _not

def test_xnor():
    compare_io(Xnor2())
    for ins in product(C.Vals, C.Vals):
        _,_, ret = Xnor2().tick(None, ins)
        if C.Vals.Q in ins:
            assert ret == [C.Vals.Q], f"{ins=}"
        elif len(set(ins)) == 2:
            assert ret == [C.Vals.L], f"{ins=}"
        else:
            assert ret == [C.Vals.H], f"{ins=}"


class Nor2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=2, nouts=1)
        self._type = "Nor2"
        self.map = {"A": 0, "B": 1}, {"Y": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        _,_, _or = Or2().tick(None, ins)
        _,_, _not = Not().tick(None, _or)
        return None, None, _not

def test_nor():
    compare_io(Nor2())
    for ins in product(C.Vals, C.Vals):
        _,_, ret = Nor2().tick(None, ins)
        if C.Vals.Q in ins:
            assert ret == [C.Vals.Q]
        elif C.Vals.H in ins:
            assert ret == [C.Vals.L]
        else:
            assert ret == [C.Vals.H]


class Nand2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=2, nouts=1)
        self._type = "Nand2"
        self.map = {"A": 0, "B": 1}, {"Y": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        _,_, _and = And2().tick(None, ins)
        _,_, _not = Not().tick(None, _and)
        return None, None, _not

def test_nand():
    compare_io(Nand2())
    for x,y in product(C.Vals, C.Vals):
        _,_, ret = Nand2().tick(None, [x,y])
        if x == y:
            if x == C.Vals.H:
                assert ret == [C.Vals.L]
            elif x == C.Vals.Q:
                assert ret == [C.Vals.Q]
            else:
                assert ret == [C.Vals.H]

class Mux2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=3, nouts=1)
        self._type = "Mux2"
        self.map = {"A0": 0, "A1": 1, "S": 2}, {"X": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        assert len(ins) == 3
        ins = tuple(ins)
        if ins[2] == C.Vals.Q:
            return None, None, [C.Vals.Q]
        elif ins[2] == C.Vals.H:
            return None, None, [ins[0]]
        return None, None, [ins[1]]

def test_mux():
    compare_io(Mux2())
    for x,y,z in product(C.Vals, C.Vals, C.Vals):
        _, _, ret = Mux2().tick(None, [x,y,z])
        if z == C.Vals.Q:
            assert ret == [C.Vals.Q]
        elif z == C.Vals.H:
            assert ret == [x]
        elif z == C.Vals.L:
            assert ret == [y]
        else:
            assert False


class And2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=2, nouts=1)
        self._type = "And2"
        self.map = {"A": 0, "B": 1}, {"X": 0}
        self.pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H]
        self.table = TWO_PORT

def test_and():
    compare_io(And2())
    for x,y in product(C.Vals, C.Vals):
        _, _, ret = And2().tick(None, [x,y])

        if C.Vals.Q in [x, y]:
            assert ret == [C.Vals.Q]
        elif C.Vals.L in [x,y]:
            assert ret == [C.Vals.L]
        else:
            assert ret == [C.Vals.H]


class Probe(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=1, nouts=1)
        self._type = "Probe"
        self.map = {"A": 0}, {"X": 0}
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

    def tick(self, _, ins):
        return None, None, ins



class Or2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=2, nouts=1)
        self._type = "Or2"
        self.map = {"A": 0, "B": 1}, {"X": 0}
        self.pattern = [C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.H]
        self.table = TWO_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

def test_or():
    compare_io(Or2())
    for x,y in product(C.Vals, C.Vals):
        _, _, ret = Or2().tick(None, [x,y])

        if C.Vals.Q in [x, y]:
            assert ret == [C.Vals.Q]
        elif C.Vals.H in [x,y]:
            assert ret == [C.Vals.H]
        else:
            assert ret == [C.Vals.L]


class Xor2(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=2, nouts=1)
        self._type = "Xor2"
        self.map = {"A": 0, "B": 1}, {"X": 0}
        self.pattern = [C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.L]
        self.table = TWO_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

def test_xor():
    compare_io(Xor2())
    for x,y in product(C.Vals, C.Vals):
        _, _, ret = Xor2().tick(None, [x,y])

        if C.Vals.Q in [x, y]:
            assert ret == [C.Vals.Q]
        elif x == y:
            assert ret == [C.Vals.L]
        else:
            assert ret == [C.Vals.H]


class Nop(C.Common):

    def __init__(self, nins, nouts):
        C.Common.__init__(self, nins=nins, nouts=nouts)
        self._type = "Nop"
        self.map = {"A": 0}, {"X": 0}

    def tick(self, _, ins):
        return None, None, ins

class Not(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=1, nouts=1)
        self._type = "Not"
        self.map = {"A": 0}, {"X": 0}
        self.pattern = [C.Vals.H, C.Vals.L]
        self.table = ONE_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

class Diode(C.Common):

    def __init__(self):
        C.Common.__init__(self, nins=1, nouts=1)
        self._type = "Diode"
        self.map = {"A": 0}, {"X": 0}
        self.pattern = [C.Vals.Q, C.Vals.H]
        self.table = ONE_PORT
        assert self.nins == len(self.map[0])
        assert self.nouts == len(self.map[1])

def test_diode():
    for x in C.Vals:
        _, _, ret = Diode().tick(None, [x])

        if x in [C.Vals.Q, C.Vals.L]:
            assert ret == [C.Vals.Q]
        else:
            assert ret == [C.Vals.H]


