module mux2(
    input wire A0,
    input wire A1,
    input wire S,
    output wire X
);
    assign X = S ? A1 : A0;
endmodule
