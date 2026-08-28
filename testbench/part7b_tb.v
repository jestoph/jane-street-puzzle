`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part7b.v */
module part7b_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [3:0] FROM_PART2;

    // Outputs
    wire [7:0] FROM_PART7B;

    reg flag;

    integer i; // 32 bit
    integer j; // 32 bit

    part7b part7a_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART20(FROM_PART2[0]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART23(FROM_PART2[3]),

      // outputs - I want part7B[6:0] to be 0x7f
      .FROM_PART7B0(FROM_PART7B[0]),
      .FROM_PART7B1(FROM_PART7B[1]),
      .FROM_PART7B2(FROM_PART7B[2]),
      .FROM_PART7B3(FROM_PART7B[3]),
      .FROM_PART7B4(FROM_PART7B[4]),
      .FROM_PART7B5(FROM_PART7B[5]),
      .FROM_PART7B6(FROM_PART7B[6]),
      .FROM_PART7B7(FROM_PART7B[7])
    );

    initial begin

        $dumpfile("waveform/part7b.vcd");
        $dumpvars(0, part7b_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | FROM_PART7[7:1]=%b", $time, FROM_PART2, OUTPUT);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
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

          if(FROM_PART7B[7:1] == 7'h7f)
          begin
            flag = 1;
          end
          if(FROM_PART7B[7:1] != 7'h7f)
          begin
            flag = 0;
          end

        end

        $finish; // End the simulation
    end

endmodule

