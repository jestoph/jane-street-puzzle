module o21bai(
    input wire A1,
    input wire A2,
    input wire B1_N,
    output wire Y
);
    assign Y = ~((A1 | A2) & (~B1_N));
endmodule
