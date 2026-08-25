module a41oi(
  input wire A1,
  input wire A2,
  input wire A3,
  input wire A4,
  input wire B1,
  output wire Y
);
    assign Y = ~((A1 & A2 & A3 & A4) | B1);
endmodule
