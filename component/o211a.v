module o211a(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire C1,
  output wire X
);
    assign X = ((A1 | A2) & B1) & C1;
endmodule
