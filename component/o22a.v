module o22a(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire B2,
  output wire X
);
    assign X = ((A1 | A2) & (B1 | B2));
endmodule
