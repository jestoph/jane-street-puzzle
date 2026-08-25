module a22o(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire B2,
  output wire X
);
    assign X = (B1 & B2) | (A1 & A2);
endmodule
