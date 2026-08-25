module o32a(
  input wire A1,
  input wire A2,
  input wire A3,
  input wire B1,
  input wire B2,
  output wire X
);
    assign X = (((A1 | A2) | A3) & (B1 | B2));
endmodule
