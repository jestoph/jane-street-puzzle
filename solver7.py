import sys
from z3 import *


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

    NUMELS = 11

    I  =  [BitVec(f'I[{i}]', 1) for i in range(121)]
    q1 =  [[BitVec(f'q1[{j}][{i}]', 1) for i in range(121) ] for j in range(NUMELS)]
    q2 =  [[BitVec(f'q2[{j}][{i}]', 1) for i in range(121) ] for j in range(NUMELS)]
    out = [[BitVec(f'out[{j}][{i}]', 1) for i in range(121)] for j in range(NUMELS)]
    part2 = [[0 for _ in range(121)] for _ in range(NUMELS)]


    for i in range(1,121):
        nxt = i
        curr = i-1

        # FROM_PART7C0 - Works!

        # assign part2[curr]  = ~ ( FROM_PART21  | FROM_PART22  | FROM_PART23  | FROM_PART20  ) ;
        part2[0][curr] = ~(PART2[curr][0] | PART2[curr][1] | PART2[curr][2] | PART2[curr][3])
        # assign FROM_PART7C0  = ( ~ q1[curr]  ) & q2[curr]  ;
        s.add(out[0][nxt] == (~q1[0][curr]) & q2[0][curr])
        # assign q1[nxt]  = ( ( q2[curr]    | (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]  ))) ;
        s.add(q1[0][nxt] == ( ( q2[0][curr] | (~ ( I[curr] & q1[0][curr] & part2[0][curr]))) & (q1[0][curr] | ( I[curr] & part2[0][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ q2[curr]   ) & (~ ( I       & q1[curr]     & part2[curr]   ))) ;
        s.add(q2[0][nxt] == ~ ( ( ~ q2[0][curr]) & (~ ( I[curr] & q1[0][curr]  & part2[0][curr]))))


        # FROM_PART7A0 - Works!

        # assign part2[curr]  = ( ~ FROM_PART22  & ~ FROM_PART20  ) & FROM_PART23  & FROM_PART21  ;
        part2[1][curr] = ~PART2[curr][0] & PART2[curr][1] & ~ PART2[curr][2] & PART2[curr][3]
        # assign FROM_PART7C0  = ( ~ q1[curr]  ) & q2[curr]  ;
        s.add(out[1][nxt] == (~q1[1][curr]) & q2[1][curr])
        # assign q1[nxt]  = ( ( q2[curr]    | (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]  ))) ;
        s.add(q1[1][nxt] == ( ( q2[1][curr] | (~ ( I[curr] & q1[1][curr] & part2[1][curr]))) & (q1[1][curr] | ( I[curr] & part2[1][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ q2[curr]   ) & (~ ( I       & q1[curr]     & part2[curr]   ))) ;
        s.add(q2[1][nxt] == ~ ( ( ~ q2[1][curr]) & (~ ( I[curr] & q1[1][curr]  & part2[1][curr]))))


        # FROM_PART7A1 - Not working

        # assign from2[curr]  = FROM_PART21  | FROM_PART22  | FROM_PART20  | ( ~ FROM_PART23  ) ;
        part2[2][curr] = PART2[curr][0] | PART2[curr][1] | PART2[curr][2] | (~PART2[curr][3])
        # assign FROM_PART7A1  = q1[curr]  & (~q2[curr])  ;
        s.add(out[2][nxt] == (q1[2][curr]) & ~q2[2][curr])
        # assign q1[nxt]  = q1[curr]    | ( q2[curr]     & (~ ( from2[curr]    | (~I      )))) ;
        s.add(q1[2][nxt] == q1[2][curr] | ( q2[2][curr]  & (~ ( part2[2][curr] | (~I[curr])))))
        # assign q2[nxt]  = ( ( q2[curr]     | (~ ( from2[curr]    | (~I)     ))) & (q1[curr]    | (~q2[curr])    | from2[curr]    | (~I      ))) ;
        s.add(q2[2][nxt] == ( ( q2[2][curr]) | (~ ( part2[2][curr] | (~I[curr]))) & (q1[2][curr] | (~q2[2][curr]) | part2[2][curr] | (~I[curr]))))


        # FROM_PART7A2 - Works!

        # assign part2[curr]  = ( ~ FROM_PART21  & ~ FROM_PART20  ) & FROM_PART23  & FROM_PART22  ;
        part2[3][curr] = ~PART2[curr][0] & ~PART2[curr][1] & PART2[curr][2] & PART2[curr][3]
        # assign FROM_PART7A2  = ( ~ q1[curr]  ) & [q2[curr]  ;
        s.add(out[3][nxt] == (~q1[3][curr]) & q2[3][curr])
        # assign q1[nxt]  = ( ( [q2[curr]  |  (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]  ))) ;
        s.add(q1[3][nxt] == ( ( q2[3][curr] | (~ ( I[curr] & q1[3][curr] & part2[3][curr]))) & (q1[3][curr] | ( I[curr] & part2[3][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ [q2[curr]  ) & (~ ( I       & q1[curr]     & part2[curr]  ))) ;
        s.add(q2[3][nxt] == ~ ( ( ~ q2[3][curr]) & (~ ( I[curr] & q1[3][curr]  & part2[3][curr]))))

        # FROM_PART7B1 - Works! Haven't tested together

        # assign part2[curr]  = FROM_PART22  | FROM_PART23  | FROM_PART20  | ( ~ FROM_PART21  ) ;
        part2[4][curr] = PART2[curr][0] | ~PART2[curr][1] | PART2[curr][2] | PART2[curr][3]
        # assign FROM_PART7B1  = q1[curr]  & (~q2[curr])  ;
        s.add(out[4][nxt] == (q1[4][curr]) & ~q2[4][curr])

        # assign q1[nxt]  = q1[curr]  | ( q2[curr]       & (~ ( part2[curr]    | (~I      )))) ;
        s.add(q1[4][nxt] == q1[4][curr] | ( q2[4][curr]  & (~ ( part2[4][curr] | (~I[curr])))))
        # assign q2[nxt]  = ( ( q2[curr]     | (~ ( part2[curr]    | (~I      )))) & (q1[curr]    | (~q2[curr])    | part2[curr]    | (~I))) ;
        s.add(q2[4][nxt] == ( ( q2[4][curr]  | (~ ( part2[4][curr] | (~I[curr])))) & (q1[4][curr] | (~q2[4][curr]) | part2[4][curr] | (~I[curr]))))

        # FROM_PARTB2 - Works!

        # assign part2[curr]  = FROM_PART21  | FROM_PART23  | FROM_PART20  | ( ~ FROM_PART22  ) ;
        part2[5][curr] = PART2[curr][0] | PART2[curr][1] | ~PART2[curr][2] | PART2[curr][3]
        # assign FROM_PART7B2  = q1[curr]  & (~q2[curr])  ;
        s.add(out[5][nxt] == (q1[5][curr]) & ~q2[5][curr])
        # assign q1[nxt]  = q1[curr]  | ( q2[curr]  & (~ ( part2[curr]  | (~I)  ))) ;
        s.add(q1[5][nxt] == q1[5][curr] | ( q2[5][curr]  & (~ ( part2[5][curr] | (~I[curr])))))
        # assign q2[nxt]  = ( ( q2[curr]  | (~ ( part2[curr]  | (~I)  ))) & (q1[curr]  | (~q2[curr])  | part2[curr]  | (~I))) ;
        s.add(q2[5][nxt] == ( ( q2[5][curr]  | (~ ( part2[5][curr] | (~I[curr])))) & (q1[5][curr] | (~q2[5][curr]) | part2[5][curr] | (~I[curr]))))


        # FROM_PART7B3 - Works!

        # assign part2[curr]  = ( ~ FROM_PART23  ) & FROM_PART20  & FROM_PART22  & FROM_PART21  ;
        part2[6][curr] = PART2[curr][0] & PART2[curr][1] & PART2[curr][2] & ~PART2[curr][3]

        # assign FROM_PART7B3  = ( ~ q1[curr]  ) & q2[curr]  ;
        s.add(out[6][nxt] == (~q1[6][curr]) & q2[6][curr])

        # assign q1[nxt]  = ( ( q2[curr]    | (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1[6][nxt] == ( ( q2[6][curr] | (~ ( I[curr] & q1[6][curr] & part2[6][curr]))) & (q1[6][curr] | ( I[curr] & part2[6][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ q2[curr]   ) & (~ ( I       & q1[curr]     & part2[curr]  ))) ;
        s.add(q2[6][nxt] == ~ ( ( ~ q2[6][curr]) & (~ ( I[curr] & q1[6][curr]  & part2[6][curr]))))



        # FROM_PART7B4 - Working!

        # assign part2[curr]  = ( ~ FROM_PART21  & ~ FROM_PART23  ) & FROM_PART20  & FROM_PART22  ;
        part2[7][curr]         = PART2[curr][0] & ~PART2[curr][1] & PART2[curr][2] & ~PART2[curr][3]
        # assign FROM_PART7B4  = ( ~ q1[curr]  ) & q2[curr]  ;
        s.add(out[7][nxt] == (~q1[7][curr]) & q2[7][curr])
        # assign q1[nxt]  = ( ( q2[curr]    | (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1[7][nxt] == ( ( q2[7][curr] | (~ ( I[curr] & q1[7][curr] & part2[7][curr]))) & (q1[7][curr] | ( I[curr] & part2[7][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ q2[curr]   ) & (~ ( I       & q1[curr]     & part2[curr]  ))) ;
        s.add(q2[7][nxt] == ~ ( ( ~ q2[7][curr]) & (~ ( I[curr] & q1[7][curr]  & part2[7][curr]))))


        # FROM_PART7B5 - Works!

        # assign part2[curr]  = ( ~ FROM_PART22  & ~ FROM_PART23  ) & FROM_PART20  & FROM_PART21  ;
        part2[8][curr]         = PART2[curr][0] & PART2[curr][1] & ~PART2[curr][2] & ~PART2[curr][3]
        # assign FROM_PART7B5  = ( ~ q1[curr]  ) & q2[curr]  ;
        s.add(out[8][nxt] == (~q1[8][curr]) & q2[8][curr])
        # assign q1[nxt]  = ( ( q2[curr]    | (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1[8][nxt] == ( ( q2[8][curr] | (~ ( I[curr] & q1[8][curr] & part2[8][curr]))) & (q1[8][curr] | ( I[curr] & part2[8][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ q2[curr]  ) & (~ ( I  & q1[curr]  & part2[curr]  ))) ;
        s.add(q2[8][nxt] == ~ ( ( ~ q2[8][curr]) & (~ ( I[curr] & q1[8][curr]  & part2[8][curr]))))


        # FROM_PART89 - Works!

        # assign part2[curr]  = ( ~ FROM_PART23  & ~ FROM_PART20  ) & FROM_PART22  & FROM_PART21  ;
        part2[9][curr]         = ~PART2[curr][0] & PART2[curr][1] & PART2[curr][2] & ~PART2[curr][3]
        # assign FROM_PART7B5  = ( ~ q1[curr]  ) & q2[curr]  ;
        s.add(out[9][nxt] == (~q1[9][curr]) & q2[9][curr])
        # assign q1[nxt]  = ( ( q2[curr]    | (~ ( I       & q1[curr]    & part2[curr]   ))) & (q1[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1[9][nxt] == ( ( q2[9][curr] | (~ ( I[curr] & q1[9][curr] & part2[9][curr]))) & (q1[9][curr] | ( I[curr] & part2[9][curr]))))
        # assign q2[nxt]  = ~ ( ( ~ q2[curr]  ) & (~ ( I  & q1[curr]  & part2[curr]  ))) ;
        s.add(q2[9][nxt] == ~ ( ( ~ q2[9][curr]) & (~ ( I[curr] & q1[9][curr]  & part2[9][curr]))))


        # FROM_PART810 -  Works!

        # assign from2[curr]  = FROM_PART21  | FROM_PART22  | FROM_PART23  | ( ~ FROM_PART20  ) ;
        part2[10][curr] = ~PART2[curr][0] | PART2[curr][1] | PART2[curr][2] | PART2[curr][3]
        # # assign FROM_PART7B2  = q1[curr]  & (~q2[curr])  ;
        s.add(out[10][nxt] == (q1[10][curr]) & ~q2[10][curr])
        # # assign q1[nxt]  = q1[curr]  | ( q2[curr]  & (~ ( part2[curr]  | (~I)  ))) ;
        s.add(q1[10][nxt] == q1[10][curr] | ( q2[10][curr]  & (~ ( part2[10][curr] | (~I[curr])))))
        # # assign q2[nxt]  = ( ( q2[curr]  | (~ ( part2[curr]  | (~I)  ))) & (q1[curr]  | (~q2[curr])  | part2[curr]  | (~I))) ;
        s.add(q2[10][nxt] == ( ( q2[10][curr]  | (~ ( part2[10][curr] | (~I[curr])))) & (q1[10][curr] | (~q2[10][curr]) | part2[10][curr] | (~I[curr]))))


    for i in range(NUMELS):
        s.add(out[i][120] == 1)

    no_empty = [x != 0 for x in I]
    # s.add(Or(*no_empty))

    if s.check() == sat:
        print("Solution!", file=sys.stderr)
        m = s.model()
        # for var in m:
        #     print(var, "|", m[var])
        for i, x in enumerate(I):
            val = m.evaluate(x, model_completion=True)
            print(f"    {i}: I = {val};")
        for i in range(NUMELS):
            val = m.evaluate(out[i][120], model_completion=True)
            print(f"    /*out[{i}]={val}|part2[{i}][120]={part2[i][120]}|part2[{i}][119]={part2[i][119]}*/")

        # print(i, x, m.evaluate("out[120]", model_completion=True))

        # for i in range(121):
        #     v = "I[{i}]"
        #     print(f"i {m[v]}")
    else:
        print("Unsatisfyable")
        sys.exit(1)


