module a21bo(
    input wire A1,
    input wire A2,
    input wire B1_N,
    output wire X
);
    assign X = ~(~(A1 & A2) & B_N); // TODO: I think this is wrong? I think should have an 'or' in there?
endmodule
