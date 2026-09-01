import sys
from z3 import *


# When clocked in the first value is 1
part2_data="""\
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 1 0
0 1 0 0
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 0
1 1 1 0
0 0 0 1
0 0 1 1
0 1 0 1
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
"""


PART2 = tuple(tuple(int(y) for y in line.split()) for line in part2_data.splitlines())

# Want it at clk120 eg data[120]

if __name__ == '__main__':
    s = Solver()


    I  =  [BitVec(f'I[{i}]', 1) for i in range(122)]
    FROM_PART7A1 = [BitVec(f'FROM_PART71A[{i}]', 1) for i in range(122)]
    Wire_522  =  [BitVec(f'Wire_522[{i}]', 1) for i in range(122)]
    q1  =  [BitVec(f'q1[{i}]', 1) for i in range(122)]
    q2  =  [BitVec(f'q2[{i}]', 1) for i in range(122)]
    Wire_516  =  [BitVec(f'Wire_516[{i}]', 1) for i in range(122)]
    Wire_4  =  [BitVec(f'Wire_4[{i}]', 1) for i in range(122)]
    Wire_514  =  [BitVec(f'Wire_514[{i}]', 1) for i in range(122)]
    Wire_515  =  [BitVec(f'Wire_515[{i}]', 1) for i in range(122)]

    # part 7a1 is unsatisfyable when these boundary conditions are set
    s.add(q1[0] == 0)
    s.add(q2[0] == 0)


    # for i in range(1,122):
    #     nxt = i
    #     curr = i-1

    #     s.add(FROM_PART7A1[curr]  == q1[curr]  & Wire_522[curr])
    #     s.add(Wire_522[curr]  == ~ q2[curr])
    #     s.add(q1[nxt]  == q1[curr]  | ( q2[curr]  & Wire_516[curr]  ))
    #     s.add(Wire_516[curr]  == ~ ( Wire_514[curr]  | Wire_515[curr]  ))
    #     s.add(q2[nxt]  == ( ( q2[curr]  | Wire_516[curr]  ) & Wire_4[curr]  ))
    #     s.add(Wire_4[curr]  == q1[curr]  | Wire_522[curr]  | Wire_514[curr]  | Wire_515[curr])
    #     # Wire_514[curr]  == FROM_PART21[curr]  | FROM_PART22[curr]  | FROM_PART20[curr]  | ( ~ FROM_PART23[curr]  )
    #     s.add(Wire_514[curr]  == PART2[curr][1]     | PART2[curr][2]     | PART2[curr][0]     | ( ~ PART2[curr][3]  ))
    #     s.add(Wire_515[curr]  == ~ ( I[curr] ))


    s.add(Sum([BV2Int(I[i]) for i in range(8, 123, 11)]) == 2)

    s.add(FROM_PART7A1[119] == 1)

    if s.check() == sat:
        print("Solution!", file=sys.stderr)
        m = s.model()
        # for var in m:
        #     print(var, "|", m[var])

        with open("out.txt", "w") as fp:
            for i, x in enumerate(I):
                val = m.evaluate(x, model_completion=True)
                print(f"    {i}: I = {val};", file=fp)

        print("verilog saved to 'out.txt'", file=sys.stderr)


        with open("data.txt", "w") as fp:
            print("clk|I|q1|q2|Wire_514|Wire_516|Wire_4|FROM_PART7A1", file=fp)
            for i in range(122):
                a = m.evaluate(q1[i], model_completion=True)
                b = m.evaluate(q2[i], model_completion=True)
                e = m.evaluate(I[i], model_completion=True)
                c = m.evaluate(Wire_514[i], model_completion=True)
                f = m.evaluate(Wire_516[i], model_completion=True)
                g = m.evaluate(Wire_4[i], model_completion=True)
                d = m.evaluate(FROM_PART7A1[i], model_completion=True)
                print(f"{i}|{e}|{a}|{b}|{c}|{f}|{g}|{d}", file=fp)

        print("data saved to 'data.txt'", file=sys.stderr)

    else:
        print("Unsatisfyable", file=sys.stderr)
        sys.exit(1)


