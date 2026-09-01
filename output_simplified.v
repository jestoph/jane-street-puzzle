// OUTPUT_SECTION
module output_section(
  input wire TO_OUTPUT0,
  input wire TO_OUTPUT1,
  input wire TO_OUTPUT2,
  input wire TO_OUTPUT3,
  input wire TO_OUTPUT4,
  input wire TO_OUTPUT5,
  input wire clk,
  input wire rst_n,
  output wire q2[curr],
  output wire q1[curr],
  output wire success
);

  // ref component/dfrtp.v
  dfrtp dfrtp_1 (
    .CLK(clk),
    .D(q1[nxt]),
    .Q(q1[curr]),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_2 (
    .CLK(clk),
    .D(q2[nxt]),
    .Q(q2[curr]),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_3 (
    .CLK(clk),
    .D(q3[nxt]),
    .Q(success),
    .RESET_B(rst_n)
  );


/*** success is q3[nxt] ***/
assign q1[nxt]  = TO_OUTPUT0  | q1[curr]
assign q2[nxt]  = ( ( ( (~ TO_OUTPUT2) & (TO_OUTPUT3  & TO_OUTPUT5)) & (( ~ q1[curr]  ) & TO_OUTPUT0  & TO_OUTPUT4  & TO_OUTPUT1)) | ( q2[curr]  & (~ ( ( ~ q1[curr]  ) & TO_OUTPUT0  ))) ) ;
assign q3[nxt]  = ( ( ( TO_OUTPUT2  & (TO_OUTPUT3  & TO_OUTPUT5)) & (( ~ q1[curr]  ) & TO_OUTPUT0  & TO_OUTPUT4  & TO_OUTPUT1)) | ( q3[nxt]  & (~ ( ( ~ q1[curr]  ) & TO_OUTPUT0  ))) ) ;

