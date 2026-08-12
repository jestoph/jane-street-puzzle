from elements.stateless import Nop, Not, And, Xor, Or, Diode, Probe
from elements.stateful import Reg
from elements.common import Common, Vals, PinType, O, I
import sys
import sqlite3

"""
TODO:
    * Make circuit description
    * Add Signal type
    * Add Bus type - Maybe just a name on a collection of wires?
"""



def dumpTable(curr, table):
    res = curr.execute(f"SELECT SQL from sqlite_master where name = ?", (table,)).fetchone()
    res = res[0]
    headers = [x.split()[0].strip() for x in res.splitlines()[1:-1]]
    res = curr.execute(f"SELECT * from {table}").fetchall()
    if not res:
        print(f"{table=} is empty")
        return

    headers = headers[:len(res[0])]

    header_row = "|".join(headers)
    print()
    print(f"Table {table}:")
    print(header_row)
    print("-" * len(header_row))
    for row in res:
        print("|".join([str(x) for x in row]))

    print()

def mkTables(curr):
    curr.execute("""
        PRAGMA foreign_keys = ON;
        """)

    # { Set up basic enum tables
    curr.execute("""
        CREATE TABLE node_types(
            type TEXT PRIMARY KEY
        );
        """)

    curr.execute("""
        INSERT INTO node_types (type)
        VALUES
        ('And'),('Or'),('Not'),('Xor'),('Reg'),('Diode'),('Nop');
        """)

    curr.execute("""
        CREATE TABLE pin_types (
            type TEXT PRIMARY KEY
        );
        """)

    curr.execute("""
        INSERT INTO pin_types (type)
        VALUES
        ('in'), ('out');
        """)

    curr.execute("""
        CREATE TABLE event_types (
            type TEXT PRIMARY KEY
        );
        """)

    curr.execute("""
        INSERT INTO event_types (type)
        VALUES
        ('rising'), ('falling');
        """)
    # } End set up basic enum tables


    curr.execute("""
        CREATE TABLE nodes (
            id INTEGER PRIMARY KEY,
            name  TEXT UNIQUE,
            node_type TEXT,
            state BLOB,                     -- Arbitrary data that a stateful node can store
            FOREIGN KEY (node_type) REFERENCES node_types(type)
        );
        """)

    curr.execute("""
        CREATE TABLE pins (
            id INTEGER PRIMARY KEY,
            nodes_id INTEGER,
            offset INTEGER NOT NULL,
            name TEXT NOT NULL,
            val TEXT NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY (nodes_id) REFERENCES nodes(id),
            FOREIGN KEY (type) REFERENCES pin_types(type)
        );
        """)

    curr.execute("""
        CREATE TABLE wires (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        """)

    curr.execute("""
        CREATE TABLE pin_wire (
            pins_id INTEGER,
            wires_id INTEGER,
            FOREIGN KEY (pins_id) REFERENCES pins(id),
            FOREIGN KEY (wires_id) REFERENCES wires(id)
        );
        """)

    curr.execute("""
        CREATE TABLE pending_inputs (
            pins_id INTEGER,
            val TEXT NOT NULL,
            tick INTEGER NOT NULL, -- the 'time' of the event
            FOREIGN KEY (pins_id) references pins(id),
            UNIQUE(pins_id, tick)
        );
        """)

    curr.execute("""
        CREATE TABLE pending_outputs (
            pins_id INTEGER,
            val TEXT NOT NULL,
            tick INTEGER NOT NULL, -- The 'time' of the event
            FOREIGN KEY (pins_id) references pins(id),
            UNIQUE(pins_id, tick)
        );
        """)

    curr.execute("""
        CREATE TABLE pending_events (
            node_id INTEGER,
            tick INTEGER NOT NULL, -- The 'time' of the event
            event_type TEXT NOT NULL,
            FOREIGN KEY (node_id) REFERENCES nodes(id),
            FOREIGN KEY (event_type) REFERENCES event_types(type),
            UNIQUE(node_id, tick)
        );
        """)
    # TODO: Add restrictions on node types


class Circuit(object): # Start Circuit {

    def __init__(self):

        self.conn = sqlite3.connect(":memory:")

        self.curr = self.conn.cursor()
        mkTables(self.curr)

        self.nodes = {}

        self._trace = False
        self.maxDepth = 10

        self.time = -1 # Start at -1?

    ################## Basic Types ###################

    def pin(self, node_id: int, offset: int, pinType: PinType, name=""):
        if not name:
            res = self.curr.execute("SELECT COALESCE(MAX(id), 1) from pins").fetchone()
            name = f"pins:__{res[0]}"

        res = self.curr.execute("""
            INSERT INTO pins (nodes_id, offset, name, val, type) VALUES (?, ?, ?, ?, ?)
        """, (node_id, offset, name, Vals.Q.value, pinType.value))

    def node(self, name: str, obj: Common) -> Nodeid:

        if not name:
            res = self.curr.execute("SELECT COALESCE(MAX(id), 1) from nodes").fetchone()
            name = f"node:__{res[0]}"


        res = self.curr.execute("""
            INSERT INTO nodes (name, node_type) values (?, ?) RETURNING id;
        """, (name, obj._type)).fetchall()

        node_id = res[0][0]

        # Register Pins
        for offset in range(obj.nins): self.pin(node_id, offset, PinType.I)
        for offset in range(obj.nouts): self.pin(node_id, offset, PinType.O)

        # Do we need this?
        self.nodes[node_id] = obj
        obj.id = node_id
        return node_id

    def wire(self, name="") -> Wireid:
        if not name:
            res = self.curr.execute("SELECT COALESCE(MAX(id) + 1, 1) from wires").fetchone()
            name = f"wire:__{res[0]}"

        res = self.curr.execute("""
            INSERT INTO wires (name) values (?) RETURNING id;
        """, (name, )).fetchall()

        wire_id = res[0][0]
        return wire_id



    ################## Node Types ##########################################

    def And(self, name=""): return self.node( name, And( 2, 1 ))
    def Or(self, name=""): return self.node( name, Or( 2, 1 ))
    def Xor(self, name=""): return self.node( name, Xor( 2, 1 ))
    def Not(self, name=""): return self.node( name, Not( 1, 1 ))
    def Diode(self, name=""): return self.node( name, Diode( 1, 1 ))

    # Probe and Signal are just syntactic sugar for passive elements
    # Where you can inject arbitrary information and read the output
    def Nop(self, name="", cnt=1): return self.node( name, Nop( cnt, cnt ))
    def Probe(self, name="", cnt=1): return self.node( name, Nop( cnt, cnt ))
    def Signal(self, name="", cnt=1): return self.node( name, Nop( cnt, cnt ))

    # Stateful Elements
    def Reg(self, name="", cnt=1): return self.node( name, Reg( cnt + 1, cnt ))
    def Clk(self, name="", period=1): return self.node(name, Clk( 0, 1, period))


    def createNode(self, name, node_type, *args):
        if node_type == 'And': return self.And(name, *args)
        if node_type == 'Or': return self.Or(name, *args)
        if node_type == 'Xor': return self.Xor(name, *args)
        if node_type == 'Not': return self.Not(name, *args)
        if node_type == 'Diode': return self.Diode(name, *args)
        if node_type == 'Reg': return self.Reg(name, *args)
        if node_type == 'Clk': return self.Reg(name, *args)
        # Probe and Signal are just syntactic sugar for passive elements
        if node_type == 'Nop': return self.Nop(name, *args)
        if node_type == 'Probe': return self.Nop(name, *args)
        if node_type == 'Signal': return self.Nop(name, *args)
        raise ValueError(f"No node type of {node_type=}")


    ########################## Getters and Setters #########################

    def getNode(self, name: str) -> Nodeid:
        res = self.curr.execute("""
            SELECT id FROM nodes WHERE name = ?
        """, (name,)).fetchone()
        if res:
            node_id = res[0]
            return node_id
        raise ValueError(f"No node named {name}")

    def _checkWritable(self, pin_id):
        res = self.curr.execute("""
            SELECT 1 from pin_wire where pins_id = ?
        """, (pin_id, )).fetchone()

        if res and len(res) > 0:
            raise ValueError('Cant write to a pin that is attached to a wire')

    def setPin(self, name, pin: I):
        return self.writePin(name, pin, Vals.H)

    def resetPin(self, name, pin):
        return self.writePin(name, pin, Vals.L)

    def togglePin(self, name, pin: I):
        if type(pin) != I:
            raise ValueError("Can't write to an out pin like this - if you really mean it you'll need to do it directly")

        node_id = self.getNode(name)
        pin_id, val = self.curr.execute("""
            SELECT id, val FROM pins where nodes_id = ? and offset = ? and type = 'in'
        """, (node_id, pin.value)).fetchone()

        self._checkWritable(pin_id)


        if val == Vals.H.value: newval = Vals.L
        elif val == Vals.L.value: newval = Vals.H
        else: newval = Vals.Q

        self.curr.execute("""
            INSERT INTO pending_inputs (pins_id, val, tick) values (?, ?, ?)
        """, (pin_id, newval.value, self.time+1))

    def writePin(self, name, pin: I, val):
        if type(pin) != I:
            raise ValueError("Can't write to an out pin like this - if you really mean it you'll need to do it directly")

        node_id = self.getNode(name)
        pin_id = self.curr.execute("""
            SELECT id FROM pins where nodes_id = ? and offset = ? and type = 'in'
        """, (node_id, pin.value)).fetchone()[0]

        self._checkWritable(pin_id)

        self.curr.execute("""
            INSERT INTO pending_inputs (pins_id, val, tick) values (?, ?, ?)
        """, (pin_id, val.value, self.time+1))

    def writePins(self, name, *args):
        assert len(args)%2 == 0, 'must have offset, val pairs'

        for i in range(len(args)//2):
            self.writePin(name, args[i*2], args[i*2+1])

    def writeReg(self, name, val):
        assert val.startswith('0b')
        vals = [Vals(x) for x in val[2:]]
        for offset, val in enumerate(vals):
            # Don't forget to skip the enable pin
            self.writePin(name, offset+1, val)

    def readProbe(self, name):
        return self.readIpin(name, I.i1)

    def readIpin(self, name, pin: I):
        node_id = self.getNode(name)

        res = self.curr.execute("""
              SELECT val FROM pins where nodes_id = ? and offset = ? and type = 'in'
        """, (node_id, pin.value)).fetchall()

        if not res[0]:
            raise ValueError(f"No ipin {pin} on node {name}")

        val = res[0][0]

        if not val:
            raise ValueError(f"No ipin {pin} on node {name}")

        return Vals(val)

    def readOPin(self, name, pin: O):
        node_id = self.getNode(name)

        res = self.curr.execute("""
              SELECT val FROM pins where nodes_id = ? and offset = ? and type = 'out'
        """, (node_id, pin.value)).fetchall()

        if not res[0]:
            raise ValueError(f"No ipin {pin} on node {name}")

        val = res[0][0]

        if not val:
            raise ValueError(f"No ipin {pin} on node {name}")

        return Vals(val)

    def nextChangedNode(self):
        res = self.curr.execute("""
            SELECT id from (
                SELECT DISTINCT nodes.id
                FROM pending_inputs pi JOIN pins ON pi.pins_id = pins.id JOIN nodes ON pins.nodes_id = nodes.id
                WHERE tick = ?
                UNION
                SELECT node_id FROM pending_events WHERE tick = ?
            ) ORDER BY RANDOM()
        """,(self.time, self.time)).fetchone()

        if res: return res[0]


    def tickNode(self, node_id):
        """
        Update the state of the node, and for any changed outputs
        move them into the pending_outputs table
        """
        pending_inputs = self.curr.execute("""
              SELECT pins.val, COALESCE(pi.val, pins.val), pins_id, pi.tick
              FROM pins LEFT JOIN pending_inputs pi
              ON pins.id = pi.pins_id
              -- tick = Null means it's not in the pending table. Tricky!
              WHERE pins.nodes_id = ? AND pins.type = 'in' AND ( tick = ? OR tick IS NULL)
              ORDER BY pins.offset ASC
        """, (node_id, self.time)).fetchall()

        node_state = self.curr.execute("""
            SELECT state FROM nodes where id = ?
        """, (node_id,)).fetchone()[0]

        self.print("*******", self.time, node_state)
        self.print(pending_inputs)
        self.dumpTable('pending_inputs')
        pending_inputs = [(a,s,d) for (a,s,d,f) in pending_inputs]

        # Update the inputs
        self.curr.executemany("""
              UPDATE pins SET val = ? where id = ?
        """, [(new_val, pin_id) for (_, new_val, pin_id) in pending_inputs])

        new_inputs = [newval for (old, newval, pin_id) in pending_inputs];

        # Update core object.
        # If new_outputs is empty that means don't update the outputs
        # If newstate is non-nil, store the state
        # If neweventoffset is non-nil, schedule a callback in neweventoffset ticks
        obj = self.nodes[node_id]
        newstate, newevents, new_outputs = obj.ticker(node_state, [Vals(val) for val in new_inputs])

        old_inputs = [x[0] for x in pending_inputs]
        self.print("TICKNODE", newstate, newevents, new_outputs, old_inputs)

        if newstate:
            self.curr.execute("""
                UPDATE nodes SET state = ? WHERE id = ?
            """, (newstate, node_id))

        if newevents:
            for event_type, offset in newevents:
                self.curr.execute("""
                    INSERT INTO pending_events (node_id, tick, event_type) VALUES (?, ?, ?)
                """, (node_id, self.time + offset, event_type))

        if new_outputs:
            self.print(f"{new_inputs=} {new_outputs=}")

            old_outputs = self.curr.execute("""
                  SELECT id, val FROM pins WHERE nodes_id = ? and type = "out"
                  ORDER BY offset ASC
            """, (node_id, )).fetchall()

            self.dumpTable("pins")

            # Write pending
            for (pin_id, old), new in zip(old_outputs, new_outputs):
                self.print(f"COMPARE {old=} {new=}")
                if old != new:
                    self.curr.execute("""
                        INSERT INTO pending_outputs (pins_id, val, tick) values (?, ?, ?)
                    """, (pin_id, new.value, self.time))

        self.print(f"UPDATE CORE - AFTER {self.time}")
        self.dumpTable("pending_inputs")
        self.dumpTable("pending_outputs")

        # Clear This node from the pending inputs
        res = self.curr.execute("""
            DELETE FROM pending_inputs WHERE pins_id IN (
                SELECT pi.pins_id
                FROM pending_inputs pi JOIN pins ON pi.pins_id = pins.id
                where pins.nodes_id = ?
            ) AND tick = ?
        """, (node_id, self.time))

        res = self.curr.execute("""
            DELETE FROM pending_events WHERE node_id = ? and tick = ?
        """, (node_id, self.time))

    def trace(self):
        self._trace = True

    def print(self, *args):
        if not self._trace: return
        print(*args)

    def tick(self):
        """
        This is an iterative recursion through the graph

        While there are pending inputs:
        1. Take all pending inputs, apply them node-by-node, and write
            any changes in the output to pending outputs
        2. Move pending outputs to pending inputs
        3. Goto 1
        """
        depth = 0
        self.time += 1

        # This handles any scheduled rising or falling edges
        self.print("BEFORE PENDING EVENT")
        self.dumpTable('pending_events')
        self.handlePendingEvents()
        self.print("AFTER PENDING EVENT")

        node_id = self.nextChangedNode()
        while node_id:

            self.print(f"Updating: {node_id=} {depth=}")
            depth += 1
            if depth > self.maxDepth:
                self.print("Recursion depth exceeded")
                break

            self.tickNode(node_id)

            node_id = self.nextChangedNode()
            self.print(f"next changed node {node_id=}")

            # If we've cleared all the inputs, its time to apply the outputs
            if node_id == None:
                self.moveOutputsToInputs()
                node_id = self.nextChangedNode()

                self.dumpTable('pending_outputs')

                if node_id == None: self.print("Really done")
                else: self.print(f"AFTER MOVING OUTPUTS TO IMPOUTS NEXT NODE Is -> {node_id}")

    def handlePendingEvent(self, node_id, event_type):

        new_inputs  = self.curr.execute("""
              SELECT val FROM pins WHERE nodes_id = ? and type = 'in' ORDER BY offset ASC
        """, (node_id, )).fetchall()

        node_state = self.curr.execute("""
            SELECT state FROM nodes where id = ?
        """, (node_id,)).fetchone()[0]

        new_inputs = [Vals(x[0]) for x in new_inputs]

        obj = self.nodes[node_id]
        newstate, newevents, new_outputs = obj.event(event_type, node_state, new_inputs)

        if newstate:
            self.curr.execute("""
                UPDATE nodes SET state = ? WHERE id = ?
            """, (newstate, node_id))

        if newevents:
            for event_type, offset in newevents:
                self.curr.execute("""
                    INSERT INTO pending_events (node_id, tick, event_type) VALUES (?, ?, ?)
                """, (node_id, self.time + offset, event_type))
            self.dumpTable('pending_events')

        if new_outputs:
            self.print(f"{new_inputs=} {new_outputs=}")

            old_outputs = self.curr.execute("""
                  SELECT id, val FROM pins WHERE nodes_id = ? and type = "out"
                  ORDER BY offset ASC
            """, (node_id, )).fetchall()

            self.dumpTable("pins")

            # Write pending
            for (pin_id, old), new in zip(old_outputs, new_outputs):
                self.print(f"COMPARE {old=} {new=}")
                if old != new:
                    self.curr.execute("""
                        INSERT INTO pending_outputs (pins_id, val, tick) values (?, ?, ?)
                    """, (pin_id, new.value, self.time))

        self.print(f"UPDATE CORE - AFTER {self.time}")
        self.dumpTable("pending_inputs")
        self.dumpTable("pending_outputs")

        # Clear This node from the pending events
        res = self.curr.execute("""
            DELETE FROM pending_events WHERE node_id = ? and tick = ?
        """, (node_id, self.time))

    def handlePendingEvents(self):
        self.print()
        self.dumpTable('pending_events')
        self.print()
        res = self.curr.execute("""
            SELECT node_id, event_type from pending_events where tick = ?
        """,(self.time,)).fetchall()

        for node_id, event_type in res:
            self.handlePendingEvent(node_id, event_type)


    def moveOutputsToInputs(self):


        # TODO: This should be a simple join but I'm too stupid
        # opins -> wire -> ipins
        opins = self.curr.execute("""
            SELECT nodes.id, pins.id, pins.offset, po.val
            FROM pending_outputs po JOIN pins ON po.pins_id = pins.id JOIN nodes ON pins.nodes_id = nodes.id
            WHERE pins.type = 'out' and po.tick = ?
        """,(self.time,)).fetchall()

        for (node_id, opin_id, offset, val) in opins:
            self.curr.execute("""
                UPDATE pins SET val = ? WHERE id = ?
            """, (val, opin_id))

            wires = self.curr.execute("""
                SELECT wires_id from pin_wire where pins_id = ?
            """, (opin_id,)).fetchall()

            for (wire_id,) in wires:
                ipins = self.curr.execute("""
                    SELECT pins_id FROM pin_wire JOIN pins
                    ON pin_wire.pins_id = pins.id
                    WHERE wires_id = ? and type = 'in'
                """, (wire_id,)).fetchall()

                self.dumpTable('pin_wire')
                self.dumpTable('pins')

                self.print(f"NEXT SET OF CHANGES {ipins} -> {val}")


                # BUG THSI IS WRONG
                self.curr.executemany("""
                    INSERT into pending_inputs (pins_id, val, tick) values (?, ?, ?)
                """,[(pin_id, val, self.time) for (pin_id,) in ipins])

            self.dumpTable('pending_inputs')

        self.curr.executemany("""
            DELETE FROM pending_outputs WHERE pins_id = ? and tick = ?
        """, [(x,self.time) for (_, x, _, _) in opins])


    def dumpTable(self, table):
        if not self._trace: return
        dumpTable(self.curr, table)

    def findWiresByPin(self, node_id, pin, pinType: PinType):
        res = self.curr.execute("""
            SELECT wires_id from pins, pin_wire where nodes_id = ? and offset = ? and type = ?
        """, (node_id, pin, pinType.value)).fetchall()

        return [x[0] for x in res]


    def attachOut(self, wireId: Wireid, nodeName: str, oPinId: I | O):
        """
        Connect a pin source to a wire - ie this pin will drive the wire
        """

        node_id = self.getNode(nodeName)

        res = self.curr.execute("""
            select id from pins where nodes_id = ? and offset = ? and type = 'out'
        """, (node_id, oPinId.value)).fetchall()

        if not res:
            raise ValueError(f"No opin '{nodeName}:{oPinId.value}'")

        pins_id = res[0][0]

        self.curr.execute("""
            INSERT INTO pin_wire (pins_id, wires_id) values (?, ?)
        """, (pins_id, wireId))

    def attachIn(self, wireId: Wireid, nodeName: str, iPinId: I | O):
        """
        Connect a pin sink to a wire - ie this pin will read from the wire
        """
        node_id = self.getNode(nodeName)

        res = self.curr.execute("""
            select id from pins where nodes_id = ? and offset = ? and type = 'in'
        """, (node_id, iPinId.value)).fetchall()

        if not res or not res[0]:
            raise ValueError(f"No ipin '{nodeName}:{iPinId.value}'")

        pins_id = res[0][0]

        self.print(f"pins {pins_id}")

        self.curr.execute("""
            INSERT INTO pin_wire (pins_id, wires_id) values (?, ?)
        """, (pins_id, wireId))

    def wireTo(self, node1, pin1, *args):
        assert len(args)%2 == 0, 'Must have an even number of args'
        w = self.wire()
        self.attachOut(w, node1, pin1)
        for i in range(len(args)//2):
            self.attachIn(w, args[i*2], args[i*2+1])

    def parseCircuit(self, desc: str):
        state  = None
        for i, line in enumerate(desc.splitlines()):

            self.print(f"{line=}")
            line = line.strip().split("#")[0].strip()

            if not line: continue

            if line == 'start-nodes':
                state = 'nodes'
                continue
            elif line == 'end-nodes':
                state = None
                continue
            elif line == 'start-wires':
                state = 'wires'
                continue
            elif line == 'end-wires':
                state = None
                continue

            if state == 'nodes':
                node, name, node_type, *extra = line.split()
                assert node == 'node', f"Expect 'node' as first arg in nodes section - {line=}"
                self.createNode(name, node_type)
                pass
            elif state == 'wires':
                src, arrow, *dst = line.split()
                src_name, src_pin = src.split(":")
                src_pin = O(int(src_pin))
                dst_pairs = []
                for x in dst:
                    print(f"{x=}")
                    l,r = x.split(":")
                    dst_pairs.append(l)
                    dst_pairs.append(I(int(r)))
                print(f"{dst_pairs=}")
                assert arrow == '->', f"Expect '->' as second arg in wires section - {nocomment=}"
                self.wireTo(src_name, src_pin, *dst_pairs)
                pass
            else:
                print("Don't know what to do in this state {state=}", line)

    def runSim(self, sim):
        for i, line in enumerate(sim.splitlines()):
            self.print(f"{line=}")
            line = line.strip().split("#")[0].strip()

            if not line: continue

            action = line.split()[0]

            if action == "set":
                action, target = line.split()
                name, pin = target.split(":")
                self.setPin(name, I(int(pin)))
            elif action == "reset":
                action, target = line.split()
                name, pin = target.split(":")
                self.resetPin(name, I(int(pin)))
            elif action == "toggle":
                action, target = line.split()
                name, pin = target.split(":")
                self.togglePin(name, I(int(pin)))
            elif action == "tick":
                self.tick()
            elif action == "time":
                action, target = line.split()
                assert self.time < int(target), "Can't set an event for the past"
                self.runTo(int(target))
            elif action == "assert":
                action, target, cmp, val = line.split()
                name, pin = target.split(":")
                targetval = self.readOPin(name, O(int(pin)))
                if cmp == '==':
                    assert targetval == Vals(val), f"Failed on {name=} at line {i}"
                elif cmp == '!=':
                    assert targetval != Vals(val), f"Failed on {name=} at line {i}"
                else:
                    raise ValueError("Unknown {cmp=}")
            else:
                raise ValueError(f"Unknown action {action}")


    def runTo(self, time)
        # TODO: Rather than simulating all time, we could just zoom right to the next pending event
        while self.time < time:
            self.tick()


    # End circuit }


#### Start Stateless Tests {

def test_double_not():# {
    c = Circuit()
    n1 = c.Not("not1")
    n2 = c.Not("not2")

    w1 = c.wire()

    c.attachOut(w1, "not1", O.o1)
    c.attachIn(w1, "not2", I.i1)

    assert c.readOPin("not2", O.o1) == Vals.Q
    c.resetPin("not1", I.i1)
    c.trace()
    c.tick()
    assert c.readOPin("not2", O.o1) == Vals.L

    c.setPin("not1", I.i1) # Write to input of first node
    assert c.readOPin("not2", O.o1) == Vals.L, "No change of input until tick"
    c.tick()
    assert c.readOPin("not2", O.o1) == Vals.H, "After tick should work"
    # }


def test_circuit_and(): # {

    c = Circuit()
    c.And("and1")

    c.writePin("and1", I.i1, Vals.H)
    assert c.readOPin("and1", O.o1) == Vals.Q, 'q and q = q'
    c.writePin("and1", I.i2, Vals.H)
    assert c.readOPin("and1", O.o1) == Vals.Q, 'Havent ticked yet'
    c.tick()
    assert c.readOPin("and1", O.o1) == Vals.H, '1 and 1 = 1'
    c.tick()
    c.tick()
    c.tick()
    assert c.readOPin("and1", O.o1) == Vals.H, 'expect no change'
    assert c.readOPin("and1", O.o1) == Vals.H, 'expect no change'
    assert c.readOPin("and1", O.o1) == Vals.H, 'expect no change'
    c.writePin("and1", I.i1, Vals.L)
    assert c.readOPin("and1", O.o1) == Vals.H, 'Havent Ticked in value'
    c.tick()
    assert c.readOPin("and1", O.o1) == Vals.L, '1 and 0 = 0'
    c.writePin("and1", I.i2, Vals.Q)
    assert c.readOPin("and1", O.o1) == Vals.L, '1 and 0 = 0'
    c.tick()
    assert c.readOPin("and1", O.o1) == Vals.Q, '1 and q = q'
    c.writePin("and1", I.i1, Vals.Q)
    c.writePin("and1", I.i2, Vals.H)
    assert c.readOPin("and1", O.o1) == Vals.Q, '1 and q = q'
    # }


def test_circuit_and1(): # {

    c = Circuit()
    a2 = c.And("and1")
    a2 = c.And("and2")

    w = c.wireTo("and1", O.o1, "and2", I.i1)

    c.setPin("and1", I.i1)
    c.setPin("and1", I.i2)
    c.tick()

    assert c.readOPin("and2", O.o1) == Vals.Q, 'One of the inputs is unknown'
    c.setPin("and2", I.i2)
    assert c.readOPin("and2", O.o1) == Vals.Q, 'One of the inputs is unknown'
    c.tick()
    assert c.readOPin("and2", O.o1) == Vals.H, '1 and 1 and 1 = 1'
    c.resetPin("and1", I.i2)
    assert c.readOPin("and2", O.o1) == Vals.H, 'havent ticked in val'
    c.tick()
    assert c.readOPin("and2", O.o1) == Vals.L, '1 and 0 and 1 = 0'
    import pytest

    with pytest.raises(ValueError):
        c.setPin("and2", I.i1)
    # }

def test_circuit_or(): # {

    c = Circuit()
    c.Or("or1")
    c.Or("or2")

    w = c.wireTo("or1", O.o1, "or2", I.i1)

    c.setPin("or1", I.i1)
    c.setPin("or1", I.i2)
    c.trace()
    c.tick()

    assert c.readOPin("or2", O.o1) == Vals.Q, 'One of the inputs is unknown'
    c.setPin("or2", I.i2)
    assert c.readOPin("or2", O.o1) == Vals.Q, 'One of the inputs is unknown'
    c.tick()
    assert c.readOPin("or2", O.o1) == Vals.H, '1 or 1 or 1 = 1'
    c.resetPin("or1", I.i2)
    assert c.readOPin("or2", O.o1) == Vals.H, 'havent ticked in val'
    c.tick()
    assert c.readOPin("or2", O.o1) == Vals.H, '1 or 0 or 1 = 1'
    c.resetPin("or1", I.i1)
    c.resetPin("or2", I.i2)
    assert c.readOPin("or2", O.o1) == Vals.H, '1 or 0 or 1 = 1'
    c.tick()
    assert c.readOPin("or2", O.o1) == Vals.L, '0 or 0 or 0 = 1'
    # }


def test_circuit_xor(): # {

    c = Circuit()
    c.Xor("xor1")
    c.Xor("xor2")

    w = c.wireTo("xor1", O.o1, "xor2", I.i1)

    c.setPin("xor1", I.i1)
    c.setPin("xor1", I.i2)
    c.tick()

    assert c.readOPin("xor2", O.o1) == Vals.Q, 'One of the inputs is unknown'
    c.setPin("xor2", I.i2)
    assert c.readOPin("xor2", O.o1) == Vals.Q, 'One of the inputs is unknown'
    c.tick()
    assert c.readOPin("xor2", O.o1) == Vals.H, '1 xor 1 xor 1 = 1'
    c.resetPin("xor1", I.i2)
    assert c.readOPin("xor2", O.o1) == Vals.H, 'havent ticked in val'
    c.tick()
    assert c.readOPin("xor2", O.o1) == Vals.L, '1 xor 0 xor 1 = 0'
    c.resetPin("xor1", I.i1)
    c.resetPin("xor2", I.i2)
    assert c.readOPin("xor2", O.o1) == Vals.L, '1 xor 0 xor 1 = 0'
    c.tick()
    c.trace()
    c.dumpTable("pins")
    assert c.readOPin("xor2", O.o1) == Vals.L, '0 xor 0 xor 0 = 0'

    c.setPin("xor1", I.i1)
    c.setPin("xor1", I.i2)
    import pytest

    with pytest.raises(ValueError):
        c.setPin("xor2", I.i1)
    # }


def test_circuit_nop(): # {

    c = Circuit()
    dut1 = c.Nop("Nop1")

    assert c.readOPin("Nop1", O.o1) == Vals.Q, 'q = q'
    c.setPin("Nop1", I.i1)
    assert c.readOPin("Nop1", O.o1) == Vals.Q, 'havent ticked yet'
    c.trace()
    c.tick()
    assert c.readOPin("Nop1", O.o1) == Vals.H, '1 = 1'
    c.resetPin("Nop1", I.i1)
    assert c.readOPin("Nop1", O.o1) == Vals.H, '1 = 1'
    c.tick()
    assert c.readOPin("Nop1", O.o1) == Vals.L, '1 = 1'
    # }

def test_circuit_not(): # {

    c = Circuit()
    dut1 = c.Not("Not1")
    i1, o1 = 0, 0

    assert c.readOPin("Not1", O.o1) == Vals.Q, 'not q = q'
    c.setPin("Not1", I.i1)
    assert c.readOPin("Not1", O.o1) == Vals.Q, 'not q = q, havent ticked yet'
    c.tick()
    assert c.readOPin("Not1", O.o1) == Vals.L, 'not 1 = 0, Ticked in'
    c.resetPin("Not1", I.i1)
    assert c.readOPin("Not1", O.o1) == Vals.L, 'havent ticked in yet'
    c.trace()
    c.tick()
    assert c.readOPin("Not1", O.o1) == Vals.H, 'havent ticked in yet'
    # }


def test_circuit_diode(): # {

    c = Circuit()
    dut1 = c.Diode("d1")
    dut1 = c.Diode("d2")


    w = c.wireTo("d1", O.o1, "d2", I.i1)

    import pytest
    with pytest.raises(ValueError):
        c.setPin("d1", O.o1)

    c.trace()
    c.setPin("d1", I.i1)
    assert c.readOPin("d2", O.o1) == Vals.Q, 'Undefined before tick'
    c.tick()
    assert c.readOPin("d2", O.o1) == Vals.H, 'High when driven'
    c.resetPin("d1", I.i1)
    c.tick()
    assert c.readOPin("d2", O.o1) == Vals.Q, 'Undefined when not driven'
    # }

#### End Stateless Tests }

#### Start Stateful Tests {

def test_circuit_reg(): # {

    c = Circuit()
    dut1 = c.Reg("r1")

    c.setPin("r1", I.i2) # i1 is the clk
    c.resetPin("r1", I.i1) # Need to initialise the clk to L before anything will happen
    assert c.readOPin("r1", O.o1) == Vals.Q, 'Undefined before tick'
    c.tick()
    assert c.readOPin("r1", O.o1) == Vals.Q, 'After as we havent clocked in val'
    c.setPin("r1", I.i1) # i1 is the clk
    c.tick()
    pending = c.curr.execute("SELECT * FROM pending_events").fetchall()
    assert len(pending) == 1, 'Never scheduled and event!'

    c.resetPin("r1", I.i1) # i1 is the clk
    assert c.readOPin("r1", O.o1) == Vals.Q, 'Havent had a rising edge yet'

    opins = c.curr.execute("SELECT * FROM pins where type = 'out'").fetchall()
    ipins = c.curr.execute("SELECT * FROM pins where type = 'in'").fetchall()

    assert len(opins) == 1, 'Should only be a single output pin'
    assert len(ipins) == 2, 'Should be two input pins'

    c.trace()
    c.tick()
    assert c.readOPin("r1", O.o1) == Vals.H, 'Finally clocked in the value'
    c.resetPin("r1", I.i2)

    assert c.readOPin("r1", O.o1) == Vals.H, 'After as we havent clocked in val'
    c.setPin("r1", I.i1)
    c.tick()
    c.resetPin("r1", I.i1) # i1 is the clk?
    assert c.readOPin("r1", O.o1) == Vals.H, 'Havent had a rising edge yet'

    # }

def test_circuit_reg1(): # {

    """
    Should take 4 ticks to propogate a signal through two serial registers
    """

    c = Circuit()
    # node clk Nop
    c.Nop("clk") # <- instead of a signal
    # node in Nop
    c.Nop("in") # <- instead of a signal
    # node r1 Nop
    c.Reg("r1")
    # node r2 Nop
    c.Reg("r2")
    # node p1 Probe
    # node p2 Probe
    c.Probe("p1")
    c.Probe("p2")

    # Wire input signal (will be low the whole time)
    # in:0 -> r1:1
    w1 = c.wireTo("in", O.o1, "r1", I.i2)

    # Wire the registers together
    # r1:0 -> r2:1
    w3 = c.wireTo("r1", O.o1, "r2", I.i2) # Place registers in series

    # Wire clock in
    # clk:0 -> r1:0
    # clk:0 -> r2:0
    c.wireTo("clk", O.o1, "r1", I.i1, "r2", I.i1)

    # Set up probes
    # r1:0 -> p1:1
    c.wireTo("r1", O.o1, "p1", I.i1)
    # r2:0 -> p2:1
    c.wireTo("r2", O.o1, "p2", I.i1)

    reg_common(c)

def reg_common(c): # {

    c.resetPin("in", I.i1)  # This stays low the whole time
    c.resetPin("clk", I.i1) # Clock just toggles, but we start low so that next tick gets a rising edge
    assert len(c.curr.execute("select * from pending_events").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 2
    assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0

    c.tick()

    assert len(c.curr.execute("select * from pending_events").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0
    assert c.time == 0
    assert c.readOPin("clk", O.o1) == Vals.L
    assert c.readOPin("in", O.o1) == Vals.L
    assert c.readOPin("r1", O.o1) == Vals.Q
    assert c.readProbe("p1") == Vals.Q
    assert c.readOPin("r2", O.o1) == Vals.Q
    assert c.readProbe("p2") == Vals.Q


    c.setPin("clk", I.i1) # Rising Edge 1
    c.tick()

    assert len(c.curr.execute("select * from pending_events").fetchall()) == 2
    assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0
    assert c.time == 1
    assert c.readOPin("clk", O.o1) == Vals.H
    assert c.readOPin("in", O.o1) == Vals.L
    assert c.readOPin("r1", O.o1) == Vals.Q
    assert c.readProbe("p1") == Vals.Q
    assert c.readOPin("r2", O.o1) == Vals.Q
    assert c.readProbe("p2") == Vals.Q

    c.resetPin("clk", I.i1)
    c.tick()  # Propogate edge

    assert len(c.curr.execute("select * from pending_events").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0
    assert c.time == 2
    assert c.readOPin("clk", O.o1) == Vals.L
    assert c.readOPin("in", O.o1) == Vals.L
    assert c.readOPin("r1", O.o1) == Vals.L
    assert c.readProbe("p1") == Vals.L
    assert c.readOPin("r2", O.o1) == Vals.Q
    assert c.readProbe("p2") == Vals.Q


    c.setPin("clk", I.i1) # Rising Edge 1
    c.tick()              # Rising Edge 1 Propogated

    assert len(c.curr.execute("select * from pending_events").fetchall()) == 2
    assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0
    assert c.time == 3
    assert c.readOPin("clk", O.o1) == Vals.H
    assert c.readOPin("in", O.o1) == Vals.L
    assert c.readOPin("r1", O.o1) == Vals.L
    assert c.readProbe("p1") == Vals.L
    assert c.readOPin("r2", O.o1) == Vals.Q
    assert c.readProbe("p2") == Vals.Q

    c.resetPin("clk", I.i1)
    c.tick()  # Propogate edge

    assert len(c.curr.execute("select * from pending_events").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 0
    assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0
    assert c.time == 4
    assert c.readOPin("clk", O.o1) == Vals.L
    assert c.readOPin("in", O.o1) == Vals.L
    assert c.readOPin("r1", O.o1) == Vals.L
    assert c.readProbe("p1") == Vals.L
    assert c.readOPin("r2", O.o1) == Vals.L
    assert c.readProbe("p1") == Vals.L

    # Should be at steady state now
    t = c.time
    for toggles in range(10):
        t += 1
        c.togglePin("clk", I.i1)
        c.tick()  # Propogate edge

        # assert len(c.curr.execute("select * from pending_events").fetchall()) == 0, toggles
        # assert len(c.curr.execute("select * from pending_inputs").fetchall()) == 0, toggles
        # assert len(c.curr.execute("select * from pending_outputs").fetchall()) == 0, toggles
        assert c.time == t, f"failed at {t}"
        assert c.readOPin("clk", O.o1) != Vals.Q, f"failed at {t}"
        assert c.readOPin("in", O.o1) == Vals.L, f"failed at {t}"
        assert c.readOPin("r1", O.o1) == Vals.L, f"failed at {t}"
        assert c.readProbe("p1") == Vals.L, f"failed at {t}"
        assert c.readOPin("r2", O.o1) == Vals.L, f"failed at {t}"
        assert c.readProbe("p1") == Vals.L, f"failed at {t}"

    # }


def test_circuit_reg_from_parse(): # {

    """
    Should take 4 ticks to propogate a signal through two serial registers
    """

    c = Circuit()
    # '#' means a comment
    desc = """
    start-nodes
        node clk Nop       # <- instead of a signal c.Nop("clk")
        node in  Nop       # <- instead of a signal c.Nop("in")
        node r1  Reg       # c.Reg("r1")
        node r2  Reg       # c.Reg("r2")
        node p1  Probe     # c.Probe("p1")
        node p2  Probe     # c.Probe("p2")
    end-nodes

    start-wires
        # Wire input signal (will be low the whole time)
        in:0 -> r1:1       # w1 = c.wireTo("in", O.o1, "r1", I.i2)

        # Wire the registers together
        r1:0 -> r2:1       # w3 = c.wireTo("r1", O.o1, "r2", I.i2) # Place registers in series

        # Wire clock in
        clk:0 -> r1:0 r2:0 # c.wireTo("clk", O.o1, "r1", I.i1, "r2", I.i1)

        # Set up probes
        r1:0 -> p1:0       # c.wireTo("r1", O.o1, "p1", I.i1)
        r2:0 -> p2:0       # c.wireTo("r2", O.o1, "p2", I.i1)
    end-wires
    """

    c.parseCircuit(desc)
    reg_common(c)

    # }

def test_circuit_sim_from_parse(): # {

    """
    Should take 4 ticks to propogate a signal through two serial registers
    """

    c = Circuit()
    # '#' means a comment
    desc = """
    start-nodes
        node clk Nop       # <- instead of a signal c.Nop("clk")
        node in  Nop       # <- instead of a signal c.Nop("in")
        node r1  Reg       # c.Reg("r1")
        node r2  Reg       # c.Reg("r2")
        node p1  Probe     # c.Probe("p1")
        node p2  Probe     # c.Probe("p2")
    end-nodes

    start-wires
        # Wire input signal (will be low the whole time)
        in:0 -> r1:1       # w1 = c.wireTo("in", O.o1, "r1", I.i2)

        # Wire the registers together
        r1:0 -> r2:1       # w3 = c.wireTo("r1", O.o1, "r2", I.i2) # Place registers in series

        # Wire clock in
        clk:0 -> r1:0 r2:0 # c.wireTo("clk", O.o1, "r1", I.i1, "r2", I.i1)

        # Set up probes
        r1:0 -> p1:0       # c.wireTo("r1", O.o1, "p1", I.i1)
        r2:0 -> p2:0       # c.wireTo("r2", O.o1, "p2", I.i1)
    end-wires
    """

    c.parseCircuit(desc)

    sim = """
    reset in:0
    reset clk:0

    tick

    assert clk:0 == L
    assert in:0 == L
    assert r1:0 == Q
    assert p1:0 == Q
    assert r2:0 == Q
    assert p2:0 == Q

    # assert c.time == 0
    # assert c.readOPin("clk", O.o1) == Vals.L
    # assert c.readOPin("in", O.o1) == Vals.L
    # assert c.readOPin("r1", O.o1) == Vals.Q
    # assert c.readProbe("p1") == Vals.Q
    # assert c.readOPin("r2", O.o1) == Vals.Q
    # assert c.readProbe("p2") == Vals.Q


    set clk:0
    tick

    # c.setPin("clk", I.i1) # Rising Edge 1
    # c.tick()

    assert clk:0 == H
    assert in:0 == L
    assert r1:0 == Q
    assert p1:0 == Q
    assert r2:0 == Q
    assert p2:0 == Q

    # assert c.time == 1
    # assert c.readOPin("clk", O.o1) == Vals.H
    # assert c.readOPin("in", O.o1) == Vals.L
    # assert c.readOPin("r1", O.o1) == Vals.Q
    # assert c.readProbe("p1") == Vals.Q
    # assert c.readOPin("r2", O.o1) == Vals.Q
    # assert c.readProbe("p2") == Vals.Q

    reset clk:0
    tick

    # c.resetPin("clk", I.i1)
    # c.tick()  # Propogate edge

    assert clk:0 == L
    assert in:0 == L
    assert r1:0 == L
    assert p1:0 == L
    assert r2:0 == Q
    assert p2:0 == Q

    # assert c.time == 2
    # assert c.readOPin("clk", O.o1) == Vals.L
    # assert c.readOPin("in", O.o1) == Vals.L
    # assert c.readOPin("r1", O.o1) == Vals.L
    # assert c.readProbe("p1") == Vals.L
    # assert c.readOPin("r2", O.o1) == Vals.Q
    # assert c.readProbe("p2") == Vals.Q

    set clk:0
    tick

    # c.setPin("clk", I.i1) # Rising Edge 1
    # c.tick()              # Rising Edge 1 Propogated

    assert clk:0 == H
    assert in:0 == L
    assert r1:0 == L
    assert p1:0 == L
    assert r2:0 == Q
    assert p2:0 == Q

    # assert c.time == 3
    # assert c.readOPin("clk", O.o1) == Vals.H
    # assert c.readOPin("in", O.o1) == Vals.L
    # assert c.readOPin("r1", O.o1) == Vals.L
    # assert c.readProbe("p1") == Vals.L
    # assert c.readOPin("r2", O.o1) == Vals.Q
    # assert c.readProbe("p2") == Vals.Q

    reset clk:0
    tick

    # c.resetPin("clk", I.i1)
    # c.tick()  # Propogate edge

    assert clk:0 == L
    assert in:0 == L
    assert r1:0 == L
    assert p1:0 == L
    assert r2:0 == L
    assert p2:0 == L

    # assert c.time == 4
    # assert c.readOPin("clk", O.o1) == Vals.L
    # assert c.readOPin("in", O.o1) == Vals.L
    # assert c.readOPin("r1", O.o1) == Vals.L
    # assert c.readProbe("p1") == Vals.L
    # assert c.readOPin("r2", O.o1) == Vals.L
    # assert c.readProbe("p1") == Vals.L

    """

    # Should be at steady state now
    for i in range(10):
        sim += """
            toggle clk:0
            tick

            assert clk:0 != Q
            assert in:0 == L
            assert r1:0 == L
            assert p1:0 == L
            assert r2:0 == L
            assert p2:0 == L

        """

    c.runSim(sim)

    # }

# } End Stateful Tests
