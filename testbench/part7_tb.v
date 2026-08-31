`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part7a.v */
/* ref outputs/part7b.v */
/* ref outputs/part7c.v */
/* ref outputs/part7.v */
module part7_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg flag;

    reg [3:0] FROM_PART2;

    // Outputs
    /* verilator lint_off UNDRIVEN */
    wire [2:0] FROM_PART7A; // Want to be 7
    wire [6:0] FROM_PART7B; // Want to be 0xfe (actually I don't think we care about the upper bit?)
    wire FROM_PART7C0;      // Not sure what we want here? I think 1?

    integer i; // 32 bit
    integer j; // 32 bit


    part7 part7_1 (

      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART20(FROM_PART2[0]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART23(FROM_PART2[3]),

      // outputs
      .FROM_PART7A0(FROM_PART7A[0]),
      .FROM_PART7A1(FROM_PART7A[1]),
      .FROM_PART7A2(FROM_PART7A[2]),

      .FROM_PART7B1(FROM_PART7B[0]),
      .FROM_PART7B2(FROM_PART7B[1]),
      .FROM_PART7B3(FROM_PART7B[2]),
      .FROM_PART7B4(FROM_PART7B[3]),
      .FROM_PART7B5(FROM_PART7B[4]),
      .FROM_PART7B6(FROM_PART7B[5]),
      .FROM_PART7B7(FROM_PART7B[6]),

      .FROM_PART7C0(FROM_PART7C0)

    );



    initial begin

        $dumpfile("waveform/part7.vcd");
        $dumpvars(0, part7_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        clk = 0;
        S = 0;
        I = 0;
        rst_n = 0;
        FROM_PART2 = 0;
        #5000; rst_n = 1;
        #5000; S=1; I=1;

        for( j = 0 ; j < 5'b10000 ; j = j + 1 )
        begin

          // #5000; rst_n = ~rst_n;
          // #5000; rst_n = ~rst_n;

          FROM_PART2 = 4'(j);

          for( i = 0 ; i < 2 ; i = i + 1 )
          begin
            #5000; clk = ~clk;
            #5000; clk = ~clk;

          end

          if(FROM_PART7B == 7'h7f)
          begin
            flag = 1;
          end
          if(FROM_PART7B != 7'h7f)
          begin
            flag = 0;
          end

        end
        I = 0;
        FROM_PART2 = 4'b0100;

        for( j = 0 ; j < 10 ; j = j + 1 )
        begin
            #5000; clk = ~clk;
            #5000; clk = ~clk;
        end


        $finish; // End the simulation
    end

endmodule
