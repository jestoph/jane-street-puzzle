module o221a(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire B2,
  input wire C1,
  output wire X
);
    assign X = (((A1 | A2) & (B1 | B2)) & C1);
endmodule
