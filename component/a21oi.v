module a21oi(
  input wire A1,
  input wire A2,
  input wire B1,
  output wire Y
);
    assign X = ~(B1 | (A1 & A2));
endmodule
