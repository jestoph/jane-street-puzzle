`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part7a.v */
module part7a_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [3:0] FROM_PART2;

    // Outputs
    wire [2:0] FROM_PART7A;

    integer i; // 32 bit
    integer j; // 32 bit

    part7a part7a_1 (
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
      .FROM_PART7A2(FROM_PART7A[2])
    );

    initial begin

        $dumpfile("waveform/part7a.vcd");
        $dumpvars(0, part7a_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);


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

        FROM_PART2 = 8;
        #5000; clk = ~clk; #5000; clk = ~clk; #5000; clk = ~clk; #5000; clk = ~clk;
        FROM_PART2 = 10;
        #5000; clk = ~clk; #5000; clk = ~clk; #5000; clk = ~clk; #5000; clk = ~clk;
        FROM_PART2 = 12;
        #5000; clk = ~clk; #5000; clk = ~clk; #5000; clk = ~clk; #5000; clk = ~clk;
        #20000;


        $finish; // End the simulation
    end

endmodule

