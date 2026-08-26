module a22oi(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire B2,
  output wire Y
);
    assign Y = ~((B1 & B2) | (A1 & A2));
endmodule
