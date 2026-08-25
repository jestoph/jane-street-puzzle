module a311o(
  input wire A1,
  input wire A2,
  input wire A3,
  input wire B1,
  input wire C1,
  output wire X
);
    assign X = ((((A1 & A2) & A3) | C1) | B1);
endmodule
