module or3b(
  input wire A,
  input wire B,
  input wire C_N,
  output wire X
);
    assign X = A | B | (~C_N);
endmodule
