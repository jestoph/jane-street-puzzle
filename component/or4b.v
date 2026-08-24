module or4b(
  input wire A,
  input wire B,
  input wire C,
  input wire D_N,
  output wire X
);
    assign X = A | B | C | (~D_N);
endmodule
