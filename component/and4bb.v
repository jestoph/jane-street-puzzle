module and4bb(
    input wire A_N,
    input wire B_N,
    input wire C,
    input wire D,
    output wire X
);
    assign X = (~A_N & ~B_N) & C & D;
endmodule
