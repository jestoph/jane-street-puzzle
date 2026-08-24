module nor3b(
  input wire A,
  input wire B,
  input wire C_N,
  output wire Y
);
    assign Y = ~(A | B | (~C_N));
endmodule
