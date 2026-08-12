from enum import Enum

from . import common as C


class And(C.Common):

    @property
    def _type(self): return "And"

    def ticker(self, state, ivals):
        assert len(ivals) == 2

        ins = set(ivals)
        if ins == {C.Vals.H}:
            return None, None, [C.Vals.H]
        elif ins == {C.Vals.L, C.Vals.H}:
            return None, None, [C.Vals.L]
        elif ins == {C.Vals.L}:
            return None, None, [C.Vals.L]
        return None, None, [C.Vals.Q]

class Probe(C.Common):

    @property
    def _type(self): return "Probe"

    def ticker(self, state, ivals):
        return None, None, ivals



class Or(C.Common):

    @property
    def _type(self): return "Or"

    def ticker(self, state, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if ins == {C.Vals.H}:
            return None, None, [C.Vals.H]
        elif ins == {C.Vals.L, C.Vals.H}:
            return None, None, [C.Vals.H]
        elif ins == {C.Vals.L}:
            return None, None, [C.Vals.L]
        return None, None, [C.Vals.Q]



class Xor(C.Common):

    @property
    def _type(self): return "Xor"

    def ticker(self, state, ivals):
        assert len(ivals) == 2
        ins = set(ivals)
        if ins == {C.Vals.H}:
            return None, None, [C.Vals.L]
        elif ins == {C.Vals.L, C.Vals.H}:
            return None, None, [C.Vals.H]
        elif ins == {C.Vals.L}:
            return None, None, [C.Vals.L]
        return None, None, [C.Vals.Q]


class Nop(C.Common):

    @property
    def _type(self): return "Nop"

    def ticker(self, state, ivals):
        return None, None, ivals

class Not(C.Common):

    @property
    def _type(self): return "Not"

    def ticker(self, state, ivals):
        assert len(ivals) == 1
        ins = set(ivals)
        if ins == {C.Vals.H}:
            return None, None, [C.Vals.L]
        elif ins == {C.Vals.L}:
            return None, None, [C.Vals.H]
        return None, None, [C.Vals.Q]


class Diode(C.Common):

    @property
    def _type(self): return "Diode"

    def ticker(self, state, ivals: [C.Vals]) -> [C.Vals]:
        assert len(ivals) == 1
        ins = set(ivals)
        if ins == {C.Vals.H}:
            return None, None, [C.Vals.H]
        return None, None, [C.Vals.Q]

