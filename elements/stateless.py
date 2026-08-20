from enum import Enum

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



"""
o21bai
a31o
a21o
a21boi
a21bo
xnor2
nand2
nor2
xor2
or2
and2
"""

class O21bai(C.Common):

    @property
    def _type(self): return "O21bai"

    @property
    def map(self): return {"A1": 0, "A2": 1, "B1_N": 2}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [
            C.Vals.H, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H
        ]
        return None, None, { x:[y] for x,y in zip(THREE, pattern) }[ins]

class A31o(C.Common):

    @property
    def _type(self): return "A31o"

    @property
    def map(self): return {"A1": 0, "A2": 1, "A3": 2, "B1": 3}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [
            C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H,
            C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H,
        ]
        return None, None, { x:[y] for x,y in zip(FOUR_PORT, pattern) }[ins]

class A21o(C.Common):

    @property
    def _type(self): return "A21o"

    @property
    def map(self): return {"A1": 0, "A2": 1, "B": 2}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H]
        return None, None, { x:[y] for x,y in zip(THREE_PORT, pattern) }[ins]

class A21boi(C.Common):

    @property
    def _type(self): return "A21boi"

    @property
    def map(self): return {"A1": 0, "A2": 1, "B_N": 2}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.H, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H]
        return None, None, { x:[y] for x,y in zip(THREE_PORT, pattern) }[ins]

class A21bo(C.Common):

    @property
    def _type(self): return "A21bo"

    @property
    def map(self): return {"A1": 0, "A2": 1, "B_N": 2}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L]
        return None, None, { x:[y] for x,y in zip(THREE_PORT, pattern) }[ins]


class Xnor2(C.Common):

    @property
    def _type(self): return "Xnor2"

    @property
    def map(self): return {"A": 0, "B": 1, "B_N": 2}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 3
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        # pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H, C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.L]
        return None, None, { x:[y] for x,y in zip(THREE_PORT, pattern) }[ins]



class Nor2(C.Common):

    @property
    def _type(self): return "Nor2"

    @property
    def map(self): return {"A": 0, "B": 1}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H]
        return None, None, { x:[y] for x,y in zip(TWO_PORT, pattern) }[ins]

class Nand2(C.Common):

    @property
    def _type(self): return "Nand2"

    @property
    def map(self): return {"A": 0, "B": 1}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H]
        return None, None, { x:[y] for x,y in zip(TWO_PORT, pattern) }[ins]



class And2(C.Common):

    @property
    def _type(self): return "And2"

    @property
    def map(self): return {"A": 0, "B": 1}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.L, C.Vals.L, C.Vals.H]
        return None, None, { x:[y] for x,y in zip(TWO_PORT, pattern) }[ins]

class Probe(C.Common):

    @property
    def _type(self): return "Probe"

    def ticker(self, _, ivals):
        return None, None, ivals



class Or2(C.Common):

    @property
    def _type(self): return "Or2"

    @property
    def map(self): return {"A": 0, "B": 1}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.H]
        return None, None, { x:[y] for x,y in zip(TWO_PORT, pattern) }[ins]




class Xor2(C.Common):

    @property
    def _type(self): return "Xor2"

    @property
    def map(self): return {"A": 0, "B": 1}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 2
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]

        pattern = [C.Vals.L, C.Vals.H, C.Vals.H, C.Vals.L]
        return None, None, { x:[y] for x,y in zip(TWO_PORT, pattern) }[ins]


class Nop(C.Common):

    @property
    def _type(self): return "Nop"

    @property
    def map(self): return {"A": 0}, {"X": 0}

    def ticker(self, _, ivals):
        return None, None, ivals

class Not(C.Common):

    @property
    def _type(self): return "Not"

    @property
    def map(self): return {"A": 0}, {"X": 0}

    def ticker(self, _, ivals):
        assert len(ivals) == 1
        ins = tuple(ivals)
        if C.Vals.Q in ins:
            return None, None, [C.Vals.Q]
        pattern = [C.Vals.H, C.Vals.L]
        return None, None, { x:[y] for x,y in zip(ONE_PORT, pattern) }[ins]


class Diode(C.Common):

    @property
    def _type(self): return "Diode"

    @property
    def map(self): return {"A": 0}, {"X": 0}

    def ticker(self, _, ivals: [C.Vals]) -> [C.Vals]:
        assert len(ivals) == 1
        ins = set(ivals)
        if ins == {C.Vals.H}:
            return None, None, [C.Vals.H]
        return None, None, [C.Vals.Q]

