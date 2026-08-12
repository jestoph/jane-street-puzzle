from enum import Enum, auto

class Vals(Enum):
    L = 'L'
    H = 'H'
    Q = 'Q' # Unknown

class EventType(Enum):
    rising = 'rising'
    falling = 'falling'


class Pinid(int): pass
class Nodeid(int): pass
class Wireid(int): pass

class Common(object):

    def __init__(self, nins: int, nouts: int):
        self.nins = nins
        self.nouts = nouts
        self.id = None


class PinType(Enum):
    O = "out"
    I = "in"

class O(Enum):
    o1 = 0
    o2 = auto()
    o3 = auto()
    o4 = auto()
    o5 = auto()
    o6 = auto()
    # 6 should be enough for anyone

class I(Enum):
    i1 = 0
    i2 = auto()
    i3 = auto()
    i4 = auto()
    i5 = auto()
    i6 = auto()
    # 6 should be enough for anyone
