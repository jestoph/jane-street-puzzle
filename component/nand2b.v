module nand2b(
  input wire A_N,
  input wire B,
  output wire Y
);
    assign Y = ~((~A_N) & B); // Syntax?
endmodule
