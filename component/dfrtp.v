module dfrtp(
    input wire D,
    input wire CLK,
    input wire RESET_B,
    output wire Q
);
  always @(posedge CLK or negedge RESET_B) begin
      if (RESET_B) begin
          Q <= 1'b0;
      end else begin
          Q <= D;
      end
  end
endmodule
