`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part1.v */
/* ref outputs/part2.v */
/* ref outputs/part3.v */
/* ref outputs/part7.v */
module part1237_tb;

    // Inputs
    reg rst_n;
    reg clk;
    reg enable;
    reg I;

    // Outputs
    // These are always opposite when enable=1
    // Otherwise, S is low and TO_OUTPUT0 is just latched to whatever it was
    wire TO_OUTPUT0;
    wire S;
    wire [4:0] FROM_PART3;
    wire [4:0] FROM_PART2;

    /* verilator lint_off UNDRIVEN */
    wire [2:0] FROM_PART7A; // Want to be 7
    wire [6:0] FROM_PART7B; // Want to be 0xfe (actually I don't think we care about the upper bit?)
    wire FROM_PART7C0;      // Want to be 1

    integer i; // 32 bit

    /* ref outputs/part1.v */
    part1 part1_1 (
      // inputs
      .rst_n(rst_n),
      .clk(clk),
      .enable(enable),
      .FROM_PART34(FROM_PART3[4]),
      .FROM_PART24(FROM_PART2[4]),
      // outputs
      .TO_OUTPUT0(TO_OUTPUT0),
      .S(S)
    );

    /* ref outputs/part2.v */
    part2 part2_1 (
      // inputs
      .rst_n(rst_n),
      .clk(clk),
      .S(S),
      // outputs
      .FROM_PART24(FROM_PART2[4]),
      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART20(FROM_PART2[0])
    );

    /* ref outputs/part3.v */
    part3 part3_1 (
      // inputs
      .rst_n(rst_n),
      .clk(clk),
      .FROM_PART24(FROM_PART2[4]),
      .S(S),
      // outputs
      .FROM_PART34(FROM_PART3[4]),
      .FROM_PART33(FROM_PART3[3]),
      .FROM_PART32(FROM_PART3[2]),
      .FROM_PART31(FROM_PART3[1]),
      .FROM_PART30(FROM_PART3[0])
    );

    part7 part7_1 (
      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART20(FROM_PART2[0]),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),
      .I(I),

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

        $dumpfile("waveform/part1237.vcd");
        $dumpvars(0, part1237_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, enable, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        rst_n = 0;
        enable = 0;
        I = 0;
        #5000; rst_n = 1;
        #5000; enable = 1;

        for(i = 0; i < 122 ; i = i + 1)
        begin

          // I=0;
          if(i == 90)
          begin
            I = 1;
          end
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end


        $finish; // End the simulation
    end

endmodule

