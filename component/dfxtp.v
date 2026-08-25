module dfxtp(
  input wire CLK,
  input wire D,
  output wire Q
);
  reg tmp;
  always @(posedge CLK) begin
      tmp <= D; // TODO: This is a guess!
  end
  assign Q = tmp;
endmodule
