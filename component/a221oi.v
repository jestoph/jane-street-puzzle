module a221oi(
  input wire A1,
  input wire A2,
  input wire B1,
  input wire B2,
  input wire C1,
  output wire Y
);
    assign Y = ~(((A1 & A2) | (B1 & B2)) | C1);
endmodule
