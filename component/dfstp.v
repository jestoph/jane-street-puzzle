module dfstp(
  input wire CLK,
  input wire D,
  input wire SET_B,
  output wire Q
);
  reg tmp;
  always @(posedge CLK or negedge SET_B) begin
      if (!SET_B) begin
          tmp <= 1'b1; // TODO: This is a guess!
      end else begin
          tmp <= D;
      end
  end
  assign Q = tmp;
endmodule
