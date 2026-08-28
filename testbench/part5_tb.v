`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part5.v */
module part5_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [5:0] FROM_PART2;
    reg Hello;

    // Outputs
    wire OUTPUT;
    wire [2:0] FROM_PART5;

    integer i; // 32 bit
    integer j; // 32 bit

    part5 part5_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART20(FROM_PART2[0]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART24(FROM_PART2[4]),

      .FROM_PART50(FROM_PART5[0]),
      .FROM_PART51(FROM_PART5[1]),
      .FROM_PART52(FROM_PART5[2]),

      .TO_OUTPUT3(OUTPUT)
    );

    initial begin

        $dumpfile("waveform/part5.vcd");
        $dumpvars(0, part5_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S = 0;
        I = 0;
        rst_n = 0;
        Hello = 0;
        FROM_PART2 = 0;
        #5000; rst_n = 1;
        #5000; S=1; I=1;

        for( j = 0; j < 6'b100000; j = j + 1)
        begin
          #5000; rst_n = 0;
          #5000; rst_n = 1;

          #5000; FROM_PART2 = j;

          #5000; clk = ~clk;
          #5000; clk = ~clk;

          `assertn(OUTPUT, FROM_PART2[4], "Output is opposite of bit 5");

        end


        $finish; // End the simulation
    end

endmodule

