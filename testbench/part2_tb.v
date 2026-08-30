`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part2.v */
module part2_tb;

    // Inputs
    reg rst_n;
    reg clk;
    reg S;

    wire [4:0] FROM_PART2;


    integer i; // 32 bit

    part2 part2_1 (
      .rst_n(rst_n),
      .clk(clk),
      .S(S),
      .FROM_PART24(FROM_PART2[4]),
      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART20(FROM_PART2[0])
    );

    initial begin

        $dumpfile("waveform/part2.vcd");
        $dumpvars(0, part2_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; S = 1;
        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end
        #5000; S = 0;
        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end
        #5000; S = 1;
        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end

        $finish; // End the simulation
    end

endmodule

