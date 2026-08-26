module o21ai(
  input wire A1,
  input wire A2,
  input wire B1,
  output wire Y
);
    assign Y = ~((A1 | A2) & B1);
endmodule
