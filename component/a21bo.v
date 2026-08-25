module a21bo(
    input wire A1,
    input wire A2,
    input wire B1_N,
    output wire X
);
    // https://sky130-unofficial.readthedocs.io/en/latest/contents/libraries/sky130_fd_sc_hd/cells/a21bo/README.html
    assign X = ~(~(A1 & A2) & B1_N);
endmodule


// | A0 | A1 | B1_N | X
// ---------------------
// | 0  | 0  | 0    | 1
// | 1  | 0  | 0    | 1
// | 0  | 1  | 0    | 1
// | 1  | 1  | 0    | 1
// | 0  | 0  | 1    | 0
// | 1  | 0  | 1    | 0
// | 0  | 1  | 1    | 0
// | 1  | 1  | 1    | 1
