module dfrtp(
  input wire D,
  input wire CLK,
  input wire RESET_B,
  output wire Q
);
  reg tmp;
  always @(posedge CLK or negedge RESET_B) begin
      if (!RESET_B) begin
          tmp <= 1'b0;
      end else begin
          tmp <= D;
      end
  end
  assign Q = tmp;
endmodule
