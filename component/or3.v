module or3(
  input wire A,
  input wire B,
  input wire C,
  output wire X
);
    assign X = A | B | C;
endmodule
