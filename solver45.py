

import sys
from z3 import *


# TODO: Spot check this data
part5_data="""\
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
1	1	1
0	1	1
1	0	1
1	1	1
"""

part5 = tuple(tuple(int(y) for y in line.split()) for line in part5_data.splitlines())

# Want it at clk120 eg data[120]

if __name__ == '__main__':
    s = Solver()

    I  =  [BitVec(f'I[{i}]', 1) for i in range(123)]
    sr =  [[BitVec(f'sr[{j}][{i}]', 1) for i in range(123) ] for j in range(12)]
    out =  [BitVec(f'out[{i}]', 1) for i in range(123)]

    # This works for TO_OUTPUT3
    i = 11
    while i < 123:
        # Have to case a Int otherwise it truncates the addition
        s.add(Sum([BV2Int(x) for x in I[i-11:i]]) == 2)
        i += 11

    # The rest is for TO_OUTPUT2
    for j in range(12):
        s.add(sr[j][0] == 0)

    for i in range(1,122):
        nxt = i
        curr = i-1

        # Shift register behaviour
        sr[0][nxt] = I[curr]
        for j in range(1, 12):
            sr[j][nxt] = sr[j-1][curr]

        # The comparison against current values
        or1 = part5[curr][0] & sr[9][curr]
        or2 = part5[curr][2] & sr[10][curr]
        or3 = part5[curr][1] & sr[0][curr]
        or4 = part5[curr][1] & sr[11][curr]

        s.add(out[curr] == ~(I[curr] & (or1 | or2 | or3 | or4)))
        s.add(out[curr] == 1)


    # TODO: What should this boundary be?
    s.add(out[119] == 1)
    s.add(out[120] == 1)
    s.add(out[121] == 1)

    if s.check() == sat:
        print("Solution!", file=sys.stderr)
        m = s.model()
        # for var in m:
        #     print(var, "|", m[var])
        # for i, x in enumerate(I):
        #     val = m.evaluate(x, model_completion=True)
        #     print(f"{val}", end='\r\n')
        for i, x in enumerate(I):
            val = m.evaluate(x, model_completion=True)
            print(f"    {i}: I = {val};")

        # print(i, x, m.evaluate("out[120]", model_completion=True))

        # for i in range(121):
        #     v = "I[{i}]"
        #     print(f"i {m[v]}")
    else:
        print("Unsatisfyable")
        sys.exit(1)


