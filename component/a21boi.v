module a21boi(
    input wire A1,
    input wire A2,
    input wire B1_N,
    output wire Y
);
    assign X = ~(~(A1 & A2) | B_N); // TODO: is this correct?
endmodule
