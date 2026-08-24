module and3b(
  input wire A_N,
  input wire B,
  input wire C,
  output wire X
);
    assign X = (~A_N) & B & C;
endmodule
