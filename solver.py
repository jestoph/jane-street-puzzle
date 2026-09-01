import sys
from z3 import *

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

    NUMELS = 11

    I  =  [BitVec(f'I[{i}]', 1) for i in range(122)]
    q1_p7 =  [[BitVec(f'q1_p7[{j}][{i}]', 1) for i in range(122) ] for j in range(NUMELS)]
    q2_p7 =  [[BitVec(f'q2_p7[{j}][{i}]', 1) for i in range(122) ] for j in range(NUMELS)]
    p7_out = [[BitVec(f'p7_out[{j}][{i}]', 1) for i in range(122)] for j in range(NUMELS)]
    part2 = [[BitVec(f'part2[{j}][{i}]', 1) for i in range(122)] for j in range(NUMELS)]

    ############################## This works for TO_OUTPUT3 ##################################
    i = 11
    while i < 123:
        # Have to case a Int otherwise it truncates the addition
        s.add(Sum([BV2Int(x) for x in I[i-11:i]]) == 2)
        i += 11

    ############################## This works for TO_OUTPUT1 ##################################
    for i in range(NUMELS):
        # part 7a1 is unsatisfyable when these boundary conditions are set
        s.add(q1_p7[i][0] == 0)
        s.add(q2_p7[i][0] == 0)

    for i in range(1,122):
        nxt = i
        curr = i-1

        # FROM_PART7C0 - Works!

        # assign part2[curr]  = ~ ( FROM_PART21  | FROM_PART22  | FROM_PART23  | FROM_PART20  ) ;
        s.add(part2[0][curr] == ~(PART2[curr][0] | PART2[curr][1] | PART2[curr][2] | PART2[curr][3]))
        # assign FROM_PART7C0  = ( ~ q1_p7[curr]  ) & q2_p7[curr]  ;
        s.add(p7_out[0][curr] == (~q1_p7[0][curr]) & q2_p7[0][curr])
        # assign q1_p7[nxt]  = ( ( q2_p7[curr]    | (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]  ))) ;
        s.add(q1_p7[0][nxt] == ( ( q2_p7[0][curr] | (~ ( I[curr] & q1_p7[0][curr] & part2[0][curr]))) & (q1_p7[0][curr] | ( I[curr] & part2[0][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ q2_p7[curr]   ) & (~ ( I       & q1_p7[curr]     & part2[curr]   ))) ;
        s.add(q2_p7[0][nxt] == ~ ( ( ~ q2_p7[0][curr]) & (~ ( I[curr] & q1_p7[0][curr]  & part2[0][curr]))))


        # FROM_PART7A0 - Works on its own, but not with the rest

        # assign part2[curr]  = ( ~ FROM_PART22  & ~ FROM_PART20  ) & FROM_PART23  & FROM_PART21  ;
        s.add(part2[1][curr] == ~PART2[curr][0] & PART2[curr][1] & ~ PART2[curr][2] & PART2[curr][3])
        # assign FROM_PART7C0  = ( ~ q1_p7[curr]  ) & q2_p7[curr]  ;
        s.add(p7_out[1][curr] == (~q1_p7[1][curr]) & q2_p7[1][curr])
        # assign q1_p7[nxt]  = ( ( q2_p7[curr]    | (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]  ))) ;
        s.add(q1_p7[1][nxt] == ( ( q2_p7[1][curr] | (~ ( I[curr] & q1_p7[1][curr] & part2[1][curr]))) & (q1_p7[1][curr] | ( I[curr] & part2[1][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ q2_p7[curr]   ) & (~ ( I       & q1_p7[curr]     & part2[curr]   ))) ;
        s.add(q2_p7[1][nxt] == ~ ( ( ~ q2_p7[1][curr]) & (~ ( I[curr] & q1_p7[1][curr]  & part2[1][curr]))))


        # !!!!! FROM_PART7A1 - Not working so handling specially down below

        # FROM_PART7A2 - Works!

        # assign part2[curr]  = ( ~ FROM_PART21  & ~ FROM_PART20  ) & FROM_PART23  & FROM_PART22  ;
        s.add(part2[3][curr] == ~PART2[curr][0] & ~PART2[curr][1] & PART2[curr][2] & PART2[curr][3])
        # assign FROM_PART7A2  = ( ~ q1_p7[curr]  ) & [q2_p7[curr]  ;
        s.add(p7_out[3][curr] == (~q1_p7[3][curr]) & q2_p7[3][curr])
        # assign q1_p7[nxt]  = ( ( [q2_p7[curr]  |  (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]  ))) ;
        s.add(q1_p7[3][nxt] == ( ( q2_p7[3][curr] | (~ ( I[curr] & q1_p7[3][curr] & part2[3][curr]))) & (q1_p7[3][curr] | ( I[curr] & part2[3][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ [q2_p7[curr]  ) & (~ ( I       & q1_p7[curr]     & part2[curr]  ))) ;
        s.add(q2_p7[3][nxt] == ~ ( ( ~ q2_p7[3][curr]) & (~ ( I[curr] & q1_p7[3][curr]  & part2[3][curr]))))

        # FROM_PART7B1 - Works!

        # assign part2[curr]  = FROM_PART22  | FROM_PART23  | FROM_PART20  | ( ~ FROM_PART21  ) ;
        s.add(part2[4][curr] == PART2[curr][0] | ~PART2[curr][1] | PART2[curr][2] | PART2[curr][3])
        # assign FROM_PART7B1  = q1_p7[curr]  & (~q2_p7[curr])  ;
        s.add(p7_out[4][curr] == (q1_p7[4][curr]) & ~q2_p7[4][curr])
        # assign q1_p7[nxt]  = q1_p7[curr]  | ( q2_p7[curr]       & (~ ( part2[curr]    | (~I      )))) ;
        s.add(q1_p7[4][nxt] == q1_p7[4][curr] | ( q2_p7[4][curr]  & (~ ( part2[4][curr] | (~I[curr])))))
        # assign q2_p7[nxt]  = ( ( q2_p7[curr]     | (~ ( part2[curr]    | (~I      )))) & (q1_p7[curr]    | (~q2_p7[curr])    | part2[curr]    | (~I))) ;
        s.add(q2_p7[4][nxt] == ( ( q2_p7[4][curr]  | (~ ( part2[4][curr] | (~I[curr])))) & (q1_p7[4][curr] | (~q2_p7[4][curr]) | part2[4][curr] | (~I[curr]))))

        # FROM_PARTB2 - Works!

        # assign part2[curr]  = FROM_PART21  | FROM_PART23  | FROM_PART20  | ( ~ FROM_PART22  ) ;
        s.add(part2[5][curr] == PART2[curr][0] | PART2[curr][1] | ~PART2[curr][2] | PART2[curr][3])
        # assign FROM_PART7B2  = q1_p7[curr]  & (~q2_p7[curr])  ;
        s.add(p7_out[5][curr] == (q1_p7[5][curr]) & ~q2_p7[5][curr])
        # assign q1_p7[nxt]  = q1_p7[curr]  | ( q2_p7[curr]  & (~ ( part2[curr]  | (~I)  ))) ;
        s.add(q1_p7[5][nxt] == q1_p7[5][curr] | ( q2_p7[5][curr]  & (~ ( part2[5][curr] | (~I[curr])))))
        # assign q2_p7[nxt]  = ( ( q2_p7[curr]  | (~ ( part2[curr]  | (~I)  ))) & (q1_p7[curr]  | (~q2_p7[curr])  | part2[curr]  | (~I))) ;
        s.add(q2_p7[5][nxt] == ( ( q2_p7[5][curr]  | (~ ( part2[5][curr] | (~I[curr])))) & (q1_p7[5][curr] | (~q2_p7[5][curr]) | part2[5][curr] | (~I[curr]))))


        # FROM_PART7B3 - Works!

        # assign part2[curr]  = ( ~ FROM_PART23  ) & FROM_PART20  & FROM_PART22  & FROM_PART21  ;
        s.add(part2[6][curr] == PART2[curr][0] & PART2[curr][1] & PART2[curr][2] & ~PART2[curr][3])
        # assign FROM_PART7B3  = ( ~ q1_p7[curr]  ) & q2_p7[curr]  ;
        s.add(p7_out[6][curr] == (~q1_p7[6][curr]) & q2_p7[6][curr])
        # assign q1_p7[nxt]  = ( ( q2_p7[curr]    | (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1_p7[6][nxt] == ( ( q2_p7[6][curr] | (~ ( I[curr] & q1_p7[6][curr] & part2[6][curr]))) & (q1_p7[6][curr] | ( I[curr] & part2[6][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ q2_p7[curr]   ) & (~ ( I       & q1_p7[curr]     & part2[curr]  ))) ;
        s.add(q2_p7[6][nxt] == ~ ( ( ~ q2_p7[6][curr]) & (~ ( I[curr] & q1_p7[6][curr]  & part2[6][curr]))))



        # FROM_PART7B4 - Working!

        # assign part2[curr]  = ( ~ FROM_PART21  & ~ FROM_PART23  ) & FROM_PART20  & FROM_PART22  ;
        s.add(part2[7][curr]  == PART2[curr][0] & ~PART2[curr][1] & PART2[curr][2] & ~PART2[curr][3])
        # assign FROM_PART7B4  = ( ~ q1_p7[curr]  ) & q2_p7[curr]  ;
        s.add(p7_out[7][curr] == (~q1_p7[7][curr]) & q2_p7[7][curr])
        # assign q1_p7[nxt]  = ( ( q2_p7[curr]    | (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1_p7[7][nxt] == ( ( q2_p7[7][curr] | (~ ( I[curr] & q1_p7[7][curr] & part2[7][curr]))) & (q1_p7[7][curr] | ( I[curr] & part2[7][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ q2_p7[curr]   ) & (~ ( I       & q1_p7[curr]     & part2[curr]  ))) ;
        s.add(q2_p7[7][nxt] == ~ ( ( ~ q2_p7[7][curr]) & (~ ( I[curr] & q1_p7[7][curr]  & part2[7][curr]))))


        # FROM_PART7B5 - Works!

        # assign part2[curr]  = ( ~ FROM_PART22  & ~ FROM_PART23  ) & FROM_PART20  & FROM_PART21  ;
        s.add(part2[8][curr]  == PART2[curr][0] & PART2[curr][1] & ~PART2[curr][2] & ~PART2[curr][3])
        # assign FROM_PART7B5  = ( ~ q1_p7[curr]  ) & q2_p7[curr]  ;
        s.add(p7_out[8][curr] == (~q1_p7[8][curr]) & q2_p7[8][curr])
        # assign q1_p7[nxt]  = ( ( q2_p7[curr]    | (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1_p7[8][nxt] == ( ( q2_p7[8][curr] | (~ ( I[curr] & q1_p7[8][curr] & part2[8][curr]))) & (q1_p7[8][curr] | ( I[curr] & part2[8][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ q2_p7[curr]  ) & (~ ( I  & q1_p7[curr]  & part2[curr]  ))) ;
        s.add(q2_p7[8][nxt] == ~ ( ( ~ q2_p7[8][curr]) & (~ ( I[curr] & q1_p7[8][curr]  & part2[8][curr]))))


        # FROM_PART7B6 - Works!

        # assign part2[curr]  = ( ~ FROM_PART23  & ~ FROM_PART20  ) & FROM_PART22  & FROM_PART21  ;
        s.add(part2[9][curr]  == ~PART2[curr][0] & PART2[curr][1] & PART2[curr][2] & ~PART2[curr][3])
        # assign FROM_PART7B6  = ( ~ q1_p7[curr]  ) & q2_p7[curr]  ;
        s.add(p7_out[9][curr] == (~q1_p7[9][curr]) & q2_p7[9][curr])
        # assign q1_p7[nxt]  = ( ( q2_p7[curr]    | (~ ( I       & q1_p7[curr]    & part2[curr]   ))) & (q1_p7[curr]    | ( I       & part2[curr]   ))) ;
        s.add(q1_p7[9][nxt] == ( ( q2_p7[9][curr] | (~ ( I[curr] & q1_p7[9][curr] & part2[9][curr]))) & (q1_p7[9][curr] | ( I[curr] & part2[9][curr]))))
        # assign q2_p7[nxt]  = ~ ( ( ~ q2_p7[curr]  ) & (~ ( I  & q1_p7[curr]  & part2[curr]  ))) ;
        s.add(q2_p7[9][nxt] == ~ ( ( ~ q2_p7[9][curr]) & (~ ( I[curr] & q1_p7[9][curr]  & part2[9][curr]))))


        # FROM_PART7B7 -  Works!

        # assign from2[curr]  = FROM_PART21  | FROM_PART22  | FROM_PART23  | ( ~ FROM_PART20  ) ;
        s.add(part2[10][curr] == ~PART2[curr][0] | PART2[curr][1] | PART2[curr][2] | PART2[curr][3])
        # # assign FROM_PART7B7  = q1_p7[curr]  & (~q2_p7[curr])  ;
        s.add(p7_out[10][curr] == (q1_p7[10][curr]) & ~q2_p7[10][curr])
        # # assign q1_p7[nxt]  = q1_p7[curr]  | ( q2_p7[curr]  & (~ ( part2[curr]  | (~I)  ))) ;
        s.add(q1_p7[10][nxt] == q1_p7[10][curr] | ( q2_p7[10][curr]  & (~ ( part2[10][curr] | (~I[curr])))))
        # # assign q2_p7[nxt]  = ( ( q2_p7[curr]  | (~ ( part2[curr]  | (~I)  ))) & (q1_p7[curr]  | (~q2_p7[curr])  | part2[curr]  | (~I))) ;
        s.add(q2_p7[10][nxt] == ( ( q2_p7[10][curr]  | (~ ( part2[10][curr] | (~I[curr])))) & (q1_p7[10][curr] | (~q2_p7[10][curr]) | part2[10][curr] | (~I[curr]))))


    # PART7A1 - you need two ticks on this frequency
    s.add(Sum([BV2Int(I[i]) for i in range(8, 123, 11)]) == 2)

    for i in range(NUMELS):
        s.add(p7_out[i][119] == 1)



    ################################## THIS WORKS FOR TO_OUTPUT2 ###############################

    sr =  [[BitVec(f'sr[{j}][{i}]', 1) for i in range(123) ] for j in range(12)]
    p4_out =  [BitVec(f'p4_out[{i}]', 1) for i in range(123)]


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

        s.add(p4_out[curr] == ~(I[curr] & (or1 | or2 | or3 | or4)))
        s.add(p4_out[curr] == 1)


    # TODO: What should this boundary be?
    s.add(p4_out[119] == 1)
    s.add(p4_out[120] == 1)
    s.add(p4_out[121] == 1)


    ################################## SEARCH FOR A SOLUTION ###############################


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
            print("clk|I|q1_p7|q2_p7|part2|p7_out", file=fp)
            for i in range(122):
                a = m.evaluate(q1_p7[2][i], model_completion=True)
                b = m.evaluate(q2_p7[2][i], model_completion=True)
                c = m.evaluate(part2[2][i], model_completion=True)
                d = m.evaluate(p7_out[2][i], model_completion=True)
                e = m.evaluate(I[i], model_completion=True)
                print(f"{i}|{e}|{a}|{b}|{c}|{d}", file=fp)

        print("data saved to 'data.txt'", file=sys.stderr)

    else:
        print("Unsatisfyable", file=sys.stderr)
        sys.exit(1)


