

import sys
from z3 import *


# Want it at clk120 eg data[120]

if __name__ == '__main__':
    s = Solver()

    I  =  [BitVec(f'I[{i}]', 1) for i in range(123)]
    TO_OUTPUT = [[BitVec(f'TO_OUTPUT[{j}][{i}]', 1) for i in range(123)] for j in range(6)]
    q1  =  [BitVec(f'q1[{i}]', 1) for i in range(122)]
    q2  =  [BitVec(f'q2[{i}]', 1) for i in range(122)]
    q3  =  [BitVec(f'q3[{i}]', 1) for i in range(122)]



    s.add(q1[0] == 0)
    s.add(q2[0] == 0)
    s.add(q3[0] == 0)

    for i in range(1,122):
        nxt = i
        curr = i-1


        # /*** success is q3[nxt] ***/
        # assign q1[nxt]  =  TO_OUTPUT0  | q1[curr]
        s.add(   q1[nxt]  == TO_OUTPUT[0][curr]  | q1[curr])
        # assign q2[nxt]  =  ( ( ( (~ TO_OUTPUT2)   & (TO_OUTPUT3    & TO_OUTPUT5))   & (( ~ q1[curr]  ) & TO_OUTPUT0    & TO_OUTPUT4    & TO_OUTPUT1))   | ( q2[curr]  & (~ ( ( ~ q1[curr]  ) & TO_OUTPUT0    ))) ) ;
        s.add(   q2[nxt]  == ( ( ( (~ TO_OUTPUT[2][curr]) & (TO_OUTPUT[3][curr]  & TO_OUTPUT[5][curr])) & (( ~ q1[curr]  ) & TO_OUTPUT[0][curr]  & TO_OUTPUT[4][curr]  & TO_OUTPUT[1][curr])) | ( q2[curr]  & (~ ( ( ~ q1[curr]  ) & TO_OUTPUT[0][curr]  ))) ))
        # assign q3[nxt]  =  ( ( ( TO_OUTPUT2    & (TO_OUTPUT3  & TO_OUTPUT5))   & (( ~ q1[curr]  ) & TO_OUTPUT0    & TO_OUTPUT4    & TO_OUTPUT1))   | ( q3[nxt]  & (~ ( ( ~ q1[curr]  ) & TO_OUTPUT0  ))) ) ;
        s.add(   q3[nxt]  == ( ( ( TO_OUTPUT[2][curr]  & (TO_OUTPUT[3][curr]  & TO_OUTPUT[5][curr])) & (( ~ q1[curr]  ) & TO_OUTPUT[0][curr]  & TO_OUTPUT[4][curr]  & TO_OUTPUT[1][curr])) | ( q3[nxt]  & (~ ( ( ~ q1[curr]  ) & TO_OUTPUT[0][curr]  ))) ))



    # TODO: What should this boundary be?
    s.add(q3[120] == 1)

    if s.check() == sat:
        print("Solution!", file=sys.stderr)
        m = s.model()

        for i in range(122):
            print(f"    {i}: begin ", end='')
            for j in range(6):
                val = m.evaluate(TO_OUTPUT[j][i], model_completion=True)
                print(f"TO_OUTPUT{j} = {val};", end='')
            print("end")

        # print(i, x, m.evaluate("out[120]", model_completion=True))

        # for i in range(121):
        #     v = "I[{i}]"
        #     print(f"i {m[v]}")
    else:
        print("Unsatisfyable")
        sys.exit(1)


