
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
/***********************************  FROM_PART80 **************************************/

// ref component/and2b.v
assign FROM_PART80  = (~q1[curr] ) & q2[curr] ;

// ref component/dfrtp.v
dfrtp dfrtp_28 (
  .CLK(clk),
  .D(q1[next]),
  .Q(q1[curr]),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_25 (
  .CLK(clk),
  .D(q2[next]),
  .Q(q2[curr]),
  .RESET_B(rst_n)
);

assign q1[next]  = ((q2[curr]  | (~(I  & q1[curr]  & blob[curr] ))) & (q1[curr]  | (I  & blob[curr] )));
assign q2[next]  = ~((~q2[curr] ) & (~(I  & q1[curr]  & blob[curr] ))); // Syntax?
// assign Wire_141  = (q1[curr]  | (I  & blob[curr] ));
// assign Wire_150  = (~(I  & q1[curr]  & blob[curr] ));

// assign blob[curr]  = ( ~ FROM_BLOB1  & ~ FROM_BLOB2  ) & FROM_BLOB3  & FROM_BLOB0  ;


"""

if __name__ == '__main__':
    s = Solver()

    I  =  [BitVec(f'I[{i}]', 1) for i in range(121)]
    q1 =  [BitVec(f'q1[{i}]', 1) for i in range(121)]
    q2 =  [BitVec(f'q2[{i}]', 1) for i in range(121)]
    out = [BitVec(f'out[{i}]', 1) for i in range(121)]


    blob = [(blob[i][0] ) & ~blob[i][1] & ~blob[i][2] & blob[i][3] for i in range(len(blob))]
    for i in range(1,121):
        nxt = i
        curr = i-1

        # assign FROM_PART810  = (~Q1_CURR ) & Q2_CURR ;
        s.add(out[i] == (~q1[curr]) & q2[curr])

        # assign q1[next]  = ((q2[curr] | (~(I[curr] & q1[curr] & blob[curr] ))) & (q1[curr] | (I[curr]  & blob[curr] )));
        s.add(q1[nxt] ==    ((q2[curr] | (~(I[curr] & q1[curr] & blob[curr] ))) & (q1[curr] | (I[curr]  & blob[curr] ))))
        # assign q2[next]  = ~((~q2[curr]) & (~(I[curr]  & q1[curr]  & blob[curr] ))); // Syntax?
        s.add(q2[nxt] ==     ~((~q2[curr]) & (~(I[curr]  & q1[curr] & blob[curr] ))))

    s.add(out[120] == 1)

    if s.check() == sat:
        print("Solution!")
        m = s.model()
        # for var in m:
        #     print(var, "|", m[var])
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


