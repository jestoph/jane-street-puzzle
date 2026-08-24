module and2b(
  input wire A_N,
  input wire B,
  output wire X
);
    assign X = (~A_N) & B;
endmodule
