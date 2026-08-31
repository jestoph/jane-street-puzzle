
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
blob = tuple(tuple(int(y) for y in line.split()) for line in blob_data.splitlines())
print(blob)

# Want it at clk120 eg data[120]

"""
THIS IS (ON OF) THE CIRCUIT(S) WE WANT TO SOLVE
/***********************************  FROM_PART88 **************************************/

// ref component/and2b.v
assign FROM_PART810  = (~Q1_CURR ) & Q2_CURR ;

assign Q1_NEXT  = ((Q2_CURR  | (~(I  & Q1_CURR  & BLOB ))) & (Q1_CURR  | ( I  & S  & BLOB  )));
assign Q2_NEXT  = ~((~Q2_CURR ) & (~(I  & Q1_CURR  & BLOB ))); // Syntax?

assign BLOB  = ( ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB0  & FROM_BLOB1  ;

"""

if __name__ == '__main__':
    s = Solver()

    I  =  [BitVec(f'I[{i}]', 1) for i in range(121)]
    q1 =  [BitVec(f'q1[{i}]', 1) for i in range(121)]
    q2 =  [BitVec(f'q2[{i}]', 1) for i in range(121)]
    out = [BitVec(f'out[{i}]', 1) for i in range(121)]


    blob = [(~blob[i][0] ) & blob[i][1] & blob[i][2] & blob[i][3] for i in range(len(blob))]
    for i in range(1,121):
        # blob_val = (1 ^ blob[i][0] ) & blob[i][1] & blob[i][2] & blob[i][3]
        curr = i
        prev = i-1

        # assign FROM_PART810  = (~Q1_CURR ) & Q2_CURR ;
        s.add(out[i] == (~q1[curr]) & q2[curr])

        # assign Q1_CURR  = ((Q2_PREV  | (~(I    & Q1_PREV  & BLOB    ))) & (Q1_PREV  | ( I    & BLOB    )));
        s.add(q1[curr] ==   ((q2[prev] | (~(I[prev] & q1[prev] & blob[prev] ))) & (q1[prev] | ( I[prev] & blob[prev] ))))
        # assign Q2_CURR = ~(  (~Q2_PREV ) & (~(I         & Q1_PREV  & BLOB ))); // Syntax?
        s.add(q2[curr] == ~((~q2[prev])  & (~I[prev]  & q1[prev] & blob[prev] )))

    s.add(out[120] == 1)

    if s.check() == sat:
        print("Solution!")
        m = s.model()
        for var in m:
            print(var, "|", m[var])
        for i, x in enumerate():
            print(i, x, m.evaluate(x, model_completion=True))
        print(i, x, m.evaluate("out[120]", model_completion=True))

        # for i in range(121):
        #     v = "I[{i}]"
        #     print(f"i {m[v]}")
    else:
        print("Unsatisfyable")


