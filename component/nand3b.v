module nand3b(
  input wire A_N,
  input wire B,
  input wire C,
  output wire Y
);
    assign Y = ~((~A_N) & B & C);
endmodule
