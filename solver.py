
from z3 import *


blob_data="""\
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 0 0 1
0 0 0 1
1 0 1 0
0 0 1 0
0 0 1 0
1 0 0 1
0 1 1 0
0 1 1 0
0 0 0 0
0 1 1 0
0 1 1 0
0 0 0 1
1 0 1 0
1 0 1 0
0 0 1 0
0 0 1 0
1 0 0 1
0 1 1 0
0 1 1 0
0 0 0 0
0 0 0 1
0 0 0 1
0 0 0 1
0 0 0 1
1 0 1 0
1 0 1 0
0 0 1 0
1 0 0 1
0 1 1 0
0 1 1 0
0 0 0 0
0 0 0 1
1 0 0 0
1 0 0 0
1 0 0 0
1 0 0 1
1 0 1 0
1 0 1 0
1 0 0 1
0 0 0 0
0 1 1 0
0 0 0 0
0 0 0 1
1 0 0 0
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
1 0 0 0
1 0 0 0
1 0 0 0
1 0 0 1
0 1 0 0
0 1 0 0
0 1 0 0
0 0 0 1
0 0 0 1
0 0 0 1
0 0 0 1
0 0 0 1
0 0 0 1
1 0 0 0
1 0 0 1
0 1 0 0
0 1 0 1
0 1 0 1
0 0 0 1
1 1 1 0
1 1 1 0
1 1 1 0
1 0 0 0
1 0 0 0
1 0 0 0
1 0 0 1
0 1 0 0
0 1 0 1
0 1 0 1
0 0 0 1
1 1 1 0
1 1 1 0
1 1 0 0
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
0 1 0 0
0 1 0 1
0 1 0 1
0 0 0 1
0 0 0 1
1 1 1 0
1 1 0 0
1 1 0 0
1 0 0 1
1 0 0 1
1 0 0 1
0 1 0 0
0 1 0 0
0 1 0 0
0 0 0 1
1 1 1 0
1 1 1 0
1 1 0 0
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
0 1 1 0
"""
BLOB = tuple(tuple(int(y) for y in line.split()) for line in blob_data.splitlines())

# Want it at clk120 eg data[120]

if __name__ == '__main__':
    s = Solver()

    NUMELS = 11

    I  =  [BitVec(f'I[{i}]', 1) for i in range(121)]
    q1 =  [[BitVec(f'q1[{i}]', 1) for i in range(121) ] for _ in range(NUMELS)]
    q2 =  [[BitVec(f'q2[{i}]', 1) for i in range(121) ] for _ in range(NUMELS)]
    out = [[BitVec(f'out[{i}]', 1) for i in range(121)] for _ in range(NUMELS)]
    blob = [[0 for _ in range(121)] for _ in range(NUMELS)]


    for i in range(1,121):
        nxt = i
        curr = i-1

        # FROM_PART80 - works individually

        # # assign blob[curr]  = ( ~ FROM_BLOB1  & ~ FROM_BLOB2  ) & FROM_BLOB3  & FROM_BLOB0  ;
        # blob[0][curr] = (BLOB[curr][0] ) & ~BLOB[curr][1] & ~BLOB[curr][2] & BLOB[curr][3]
        # # assign FROM_PART810  = (~Q1_CURR ) & Q2_CURR ;
        # s.add(out[0][nxt] == (~q1[0][curr]) & q2[0][curr])
        # # assign q1[next]  = ((q2[curr] | (~(I[curr] & q1[curr] & blob[curr] ))) & (q1[curr] | (I[curr]  & blob[curr] )));
        # s.add(q1[0][nxt] ==    ((q2[0][curr] | (~(I[curr] & q1[0][curr] & blob[0][curr] ))) & (q1[0][curr] | (I[curr]  & blob[0][curr] ))))
        # # assign q2[next]  = ~((~q2[curr]) & (~(I[curr]  & q1[curr]  & blob[curr] ))); // Syntax?
        # s.add(q2[0][nxt] ==     ~((~q2[0][curr]) & (~(I[curr]  & q1[0][curr] & blob[0][curr] ))))


        # FROM_PART81 - works individually

        # # assign blob[curr]  = (~FROM_BLOB0  & ~FROM_BLOB2 ) & FROM_BLOB3  & FROM_BLOB1 ;
        # blob[1][curr] = ~BLOB[curr][0]  & BLOB[curr][1] & ~BLOB[curr][2] & BLOB[curr][3]
        # # assign FROM_PART81  = (~q1[curr] )   & q2[curr] ;
        # s.add(out[1][nxt] ==    (~q1[1][curr]) & q2[1][curr])
        # # assign q1[nxt]  = ((q2[curr]    | (~(I[curr] & q1[curr]    & blob[curr] )))    & (q1[curr]    | (I[curr]  & blob[curr] )));
        # s.add(q1[1][nxt] == ((q2[1][curr] | (~(I[curr] & q1[1][curr] & blob[1][curr] ))) & (q1[1][curr] | (I[curr]  & blob[1][curr] ))))
        # # assign q2[nxt]  = ~((~q2[curr] )   & (~(I[curr]  & q1[curr]  & blob[curr] ))); // Syntax?
        # s.add(q2[1][nxt] == ~((~q2[1][curr]) & (~(I[curr]  & q1[1][curr] & blob[1][curr] ))))

        # FROM_PART82 - doesn't work at all ???

        # assign blob[curr]  = ( ~ FROM_BLOB3  & ~ FROM_BLOB2  ) & FROM_BLOB0  & FROM_BLOB1  ;
        blob[2][curr] = BLOB[curr][0]  & BLOB[curr][1] & ~BLOB[curr][2] & ~BLOB[curr][3]
        # # assign FROM_PART82  = (~q1[curr] ) & q2[nxt] ;
        # s.add(out[2][nxt] ==    (~q1[2][curr]) & q2[2][curr])
        # # assign q1[nxt]  = ((q2[curr]    | (~(I  & q1[curr]  & blob[curr] ))) & (q1[curr]  | (I  & blob[curr] )));
        # s.add(q1[2][nxt] == ((q2[2][curr] | (~(I[curr] & q1[2][curr] & blob[2][curr] ))) & (q1[2][curr] | (I[curr]  & blob[2][curr] ))))
        # # assign q2[nxt]  = ~((~q2[curr] ) & (~(I  & q1[curr]  & blob[curr] ))); // Syntax?
        # s.add(q2[2][nxt] == ~((~q2[2][curr]) & (~(I[curr]  & q1[2][curr] & blob[2][curr] ))))

        # assign FROM_PART812  = (~Q1_CURR ) & Q2_CURR ;
        s.add(out[2][nxt] == (~q1[2][curr]) & q2[2][curr])

        # assign q1[nxt]  = ((q2[curr]    | (~ (I       & q1[curr]    & blob[curr]    ))) & (q1[curr]    | (I        & blob[curr]  ))) ;
        s.add(q1[2][nxt] == ((q2[2][curr] | (~ (I[curr] & q1[2][curr] & blob[2][curr] ))) & (q1[2][curr] | (I[curr]  & blob[2][curr] ))))
        # assign q2[nxt]  = ~((~q2[curr]   ) & (~(I        & q1[curr]    & blob[curr]    ))) ; // Syntax?
        s.add(q2[2][nxt] == ~((~q2[2][curr]) & (~(I[curr]  & q1[2][curr] & blob[2][curr] ))))

        """

        assign FROM_PART82  = ( ~ q1[curr]  ) & q2[curr]  ;
        assign q1[nxt]  = ( ( q2[curr]  | (~ ( I  & S  & q1[curr]  & blob[curr]  ))) & (q1[curr]  | ( I  & S  & blob[curr]  ))) ;
        assign q2[nxt]  = ~ ( ( ~ q2[curr]  ) & (~ ( I  & S  & q1[curr]  & blob[curr]  ))) ; // Syntax?
        assign blob[curr]  = ( ~ FROM_BLOB3  & ~ FROM_BLOB2  ) & FROM_BLOB0  & FROM_BLOB1  ;

        assign Wire_194  = (~ ( I  & S  & q1[curr]  & blob[curr]  )) ;
        assign Wire_201  = (q1[curr]  | ( I  & S  & blob[curr]  )) ;

        """

        # FROM_PART83 - works individually

        # # assign blob[curr]  = ~ ( FROM_BLOB1  | FROM_BLOB0  | FROM_BLOB3  | FROM_BLOB2  ) ;
        # blob[3][curr] = ~ (BLOB[curr][0] | BLOB[curr][1] | BLOB[curr][2] | BLOB[curr][3])
        # # assign FROM_PART83  = (~q1[curr] ) & q2[curr] ;
        # s.add(out[3][nxt] ==    (~q1[3][curr]) & q2[3][curr])
        # # assign q1[nxt]  = ((q2[curr]  | (~(I  & q1[curr]  & blob[curr] ))) & (q1[curr]  | (I  & blob[curr] )));
        # s.add(q1[3][nxt] == ((q2[3][curr] | (~(I[curr] & q1[3][curr] & blob[3][curr] ))) & (q1[3][curr] | (I[curr]  & blob[3][curr] ))))
        # # assign q2[nxt]  = ~((~q2[curr] ) & (~(I  & q1[curr]  & blob[curr] ))); // Syntax?
        # s.add(q2[3][nxt] == ~((~q2[3][curr]) & (~(I[curr]  & q1[3][curr] & blob[3][curr] ))))


        # FROM_PART84 - works individually

        # # assign blob[curr]  = ( ~ FROM_BLOB0  & ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB1  ;
        # blob[4][curr] =  ~BLOB[curr][0] & BLOB[curr][1] & BLOB[curr][2] & ~BLOB[curr][3]
        # # assign FROM_PART84  = (~q1[curr] ) & q2[curr] ;
        # s.add(out[4][nxt] ==    (~q1[4][curr]) & q2[4][curr])
        # # assign q1[nxt]  = ((q2[curr]  | (~(I  & q1[curr]  & blob[curr] ))) & (q1[curr]  | (I  & blob[curr] )));
        # s.add(q1[4][nxt] == ((q2[4][curr] | (~(I[curr] & q1[4][curr] & blob[4][curr] ))) & (q1[4][curr] | (I[curr]  & blob[4][curr] ))))
        # # assign q2[nxt]  = ~((~q2[curr] ) & (~(I  & q1[curr]  & blob[curr] ))); // Syntax?
        # s.add(q2[4][nxt] == ~((~q2[4][curr]) & (~(I[curr]  & q1[4][curr] & blob[4][curr] ))))

        # FROM_PART85 - works individually

        # # assign blob[curr]  = FROM_BLOB1  | FROM_BLOB0  | FROM_BLOB3  | ( ~ FROM_BLOB2  ) ;
        # blob[5][curr] =  BLOB[curr][0] | BLOB[curr][1] | (~BLOB[curr][2]) | BLOB[curr][3]
        # # assign FROM_PART85  = ~q1[curr] & q2[curr];
        # s.add(out[5][nxt] ==    (~q1[5][curr]) & q2[5][curr])
        # # assign q1[nxt]  = ((q1[curr]  | (~blob[curr]      & I ))      & (q2[curr]  | ~q1[curr]  | blob[curr]  | ~I));
        # s.add(q1[5][nxt] == ((q1[5][curr] | (~blob[5][curr] & I[curr])) & (q2[5][curr] | ~q1[5][curr] | blob[5][curr] | ~I[curr])))
        # # assign q2[nxt]  = q2[curr]    | (q1[curr]    & (~blob[curr]    & I ));
        # s.add(q2[5][nxt] == q2[5][curr] | (q1[5][curr] & (~blob[5][curr] & I[curr])))

        # FROM_PART86 - works individually

        # # assign blob[curr]  = FROM_BLOB1  | FROM_BLOB0  | FROM_BLOB2  | ( ~ FROM_BLOB3  ) ;
        # blob[6][curr] =  BLOB[curr][0] | BLOB[curr][1] | (BLOB[curr][2]) | ~BLOB[curr][3]
        # # assign FROM_PART86  = ~q1[curr] & q2[curr];
        # s.add(out[6][nxt] ==    (~q1[6][curr]) & q2[6][curr])
        # # assign q1[nxt]  = ((q1[curr]  | (~blob[curr]  & I )) & (q2[curr]  | ~q1[curr]  | blob[curr]  | ~I));
        # s.add(q1[6][nxt] == ((q1[6][curr] | (~blob[6][curr] & I[curr])) & (q2[6][curr] | ~q1[6][curr] | blob[6][curr] | ~I[curr])))
        # # assign q2[nxt]  = q2[curr]  | (q1[curr]  & (~blob[curr]  & I ));
        # s.add(q2[6][nxt] == q2[6][curr] | (q1[6][curr] & (~blob[6][curr] & I[curr])))

        # FROM_PART87 - works individually

        # # assign blob[curr]  = FROM_BLOB1  | FROM_BLOB3  | FROM_BLOB2  | ( ~ FROM_BLOB0  ) ;
        # blob[7][curr] =  ~BLOB[curr][0] | BLOB[curr][1] | (BLOB[curr][2]) | BLOB[curr][3]
        # # assign FROM_PART87  = ~q1[curr] & q2[curr];
        # # assign q1[nxt]  = ((q1[curr]  | (~blob[curr]  & I )) & (q2[curr]  | ~q1[curr]  | blob[curr]  | ~I ));
        # # assign q2[nxt]  = q2[curr]  | (q1[curr]  & (~blob[curr]  & I ));
        # # assign blob[curr]  = FROM_BLOB1  | FROM_BLOB3  | FROM_BLOB2  | ( ~ FROM_BLOB0  ) ;

        # TRUE COPIED BUT ABOVE WORKS ANYWAY
        # s.add(out[7][nxt] ==    (~q1[7][curr]) & q2[7][curr])
        # # assign q1[nxt]  = ((q1[curr]  | (~blob[curr]  & I )) & (q2[curr]  | ~q1[curr]  | blob[curr]  | ~I));
        # s.add(q1[7][nxt] == ((q1[5][curr] | (~blob[7][curr] & I[curr])) & (q2[7][curr] | ~q1[7][curr] | blob[7][curr] | ~I[curr])))
        # # assign q2[nxt]  = q2[curr]  | (q1[curr]  & (~blob[curr]  & I ));
        # s.add(q2[7][nxt] == q2[7][curr] | (q1[7][curr] & (~blob[7][curr] & I[curr])))

        # FROM_PART88 - works individually

        # # assign Wire_222  = FROM_BLOB0  | FROM_BLOB3  | FROM_BLOB2  | ( ~ FROM_BLOB1  ) ;
        # blob[8][curr] =  BLOB[curr][0] | ~BLOB[curr][1] | (BLOB[curr][2]) | BLOB[curr][3]

        # s.add(out[8][nxt] ==    (~q1[8][curr]) & q2[8][curr])
        # # assign q1[nxt]  = ((q1[curr]  | (~blob[curr]  & I )) & (q2[curr]  | ~q1[curr]  | blob[curr]  | ~I));
        # s.add(q1[8][nxt] == ((q1[8][curr] | (~blob[8][curr] & I[curr])) & (q2[8][curr] | ~q1[8][curr] | blob[8][curr] | ~I[curr])))
        # # assign q2[nxt]  = q2[curr]  | (q1[curr]  & (~blob[curr]  & I ));
        # s.add(q2[8][nxt] == q2[8][curr] | (q1[8][curr] & (~blob[8][curr] & I[curr])))

        # FROM_PART89 - Works individually

        # # assign blob[curr]  = ( ~ FROM_BLOB1  & ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB0  ;
        # blob[9][curr] =  BLOB[curr][0] & ~BLOB[curr][1] & (BLOB[curr][2]) & ~BLOB[curr][3]
        # # assign FROM_PART89  = (~q1[curr] ) & q2[curr] ;
        # s.add(out[9][nxt] ==    (~q1[9][curr]) & q2[9][curr])
        # # assign q1[nxt]  = ((q2[curr]    | (~(I       & q1[curr]      & blob[curr]    ))) & (q1[curr]    | (I       & blob[curr]    )));
        # s.add(q1[9][nxt] == ((q2[9][curr] | (~(I[curr] & q1[9][curr]   & blob[9][curr] ))) & (q1[9][curr] | (I[curr] & blob[9][curr] ))))
        # # assign q2[nxt]  = ~((~q2[curr]   ) & (~(I       & q1[curr]    & blob[curr] ))); // Syntax?
        # s.add(q2[9][nxt] == ~((~q2[9][curr]) & (~(I[curr] & q1[9][curr] & blob[9][curr] ))))

        # FROM_PART89 - Works individually

        # # assign blob[curr]  = ( ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB0  & FROM_BLOB1  ;
        # blob[10][curr] =  BLOB[curr][0] & BLOB[curr][1] & (BLOB[curr][2]) & ~BLOB[curr][3]
        # # assign FROM_PART810  = (~q1[curr] ) & q2[curr] ;
        # s.add(out[10][nxt] ==    (~q1[10][curr]) & q2[10][curr])
        # # assign q1[nxt]  = ((q2[curr]  | (~(I  & q1[curr]  & blob[curr] )) ) & (q1[curr]  | ( I  & blob[curr]  )));
        # s.add(q1[10][nxt] == ((q2[10][curr] | (~(I[curr] & q1[10][curr]   & blob[10][curr] ))) & (q1[10][curr] | (I[curr] & blob[10][curr] ))))
        # # assign q2[nxt]  = ~((~q2[curr] ) & (~(I  & q1[curr]  & blob[curr] ))); // Syntax?
        # s.add(q2[10][nxt] == ~((~q2[10][curr]) & (~(I[curr] & q1[10][curr] & blob[10][curr] ))))


    for i in range(NUMELS):
        print("WARNING: TEMPORARILY CHANGED CONSTRAINTS", file=sys.stderr)
        s.add(out[i][120] == 1)

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
            print(f"    /*out[{i}] = {val}*/")

        # print(i, x, m.evaluate("out[120]", model_completion=True))

        # for i in range(121):
        #     v = "I[{i}]"
        #     print(f"i {m[v]}")
    else:
        print("Unsatisfyable")
        sys.exit(1)


