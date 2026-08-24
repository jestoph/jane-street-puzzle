module or4bb(
  input wire A,
  input wire B,
  input wire C_N,
  input wire D_N,
  output wire X
);
    assign X = A | B | (~C_N) | (~D_N);
endmodule
