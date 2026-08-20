from enum import Enum
from . import common as C


class Reg(C.Common):

    @property
    def _type(self): return "Reg"

    def tick(self, state, ivals):

        print(f"STATE {state=} {ivals=}")

        if state:
            clk = state

            if clk == C.Vals.L.value and ivals[0] == C.Vals.H:
                # Seen a rising edge - schedule a callback
                return ivals[0].value, [(C.EventType.rising.value, 1)], []

            return ivals[0].value, None, [] # Empty indicates no change

        else:
            return ivals[0].value, None, []

    def event(self, event_type, state, ivals):
        if event_type == C.EventType.rising.value:
            return ivals[0].value, None, ivals[1:]
        else:
            return None, None, None

class Clk(C.Common):

    @property
    def _type(self): return "Clk"

    def tick(self, state, ivals):

        print(f"STATE {state=} {ivals=}")

        if state:
            clk = state

            if clk == C.Vals.L.value and ivals[0] == C.Vals.H:
                # Seen a rising edge - schedule a callback
                return ivals[0].value, [(C.EventType.rising.value, 1)], []

            return ivals[0].value, None, [] # Empty indicates no change

        else:
            return ivals[0].value, None, []

    def event(self, event_type, state, ivals):
        if event_type == C.EventType.rising.value:
            return ivals[0].value, None, ivals[1:]
        else:
            return None, None, None
