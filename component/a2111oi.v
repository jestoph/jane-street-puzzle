module a2111oi(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire C1,
  input wire D1,
  output wire Y
);
    assign Y = ~((A1 & A2) | B1 | C1 | D1 );
endmodule
