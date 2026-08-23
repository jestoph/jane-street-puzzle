module a21o(
    input wire A1,
    input wire A2,
    input wire B1,
    output wire X
);
    assign X = B1 | (A1 & A2);
endmodule
