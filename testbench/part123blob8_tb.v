`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part1.v */
/* ref outputs/part2.v */
/* ref outputs/part3.v */
/* ref outputs/partblob.v */
/* ref outputs/part8.v */
module part123blob8_tb;

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
    wire [3:0] FROM_BLOB;
    wire [10:0] FROM_PART8;

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

    blob blob_1 (

      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART20(FROM_PART2[0]),

      .FROM_PART33(FROM_PART3[3]),
      .FROM_PART32(FROM_PART3[2]),
      .FROM_PART31(FROM_PART3[1]),
      .FROM_PART30(FROM_PART3[0]),

      .FROM_BLOB3(FROM_BLOB[3]),
      .FROM_BLOB2(FROM_BLOB[2]),
      .FROM_BLOB1(FROM_BLOB[1]),
      .FROM_BLOB0(FROM_BLOB[0])

    );

    part8 part8_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),


      .FROM_BLOB0(FROM_BLOB[0]),
      .FROM_BLOB1(FROM_BLOB[1]),
      .FROM_BLOB2(FROM_BLOB[2]),
      .FROM_BLOB3(FROM_BLOB[3]),

      // outputs - want this to be 11'h7ff;
      .FROM_PART80(FROM_PART8[0]),
      .FROM_PART81(FROM_PART8[1]),
      .FROM_PART82(FROM_PART8[2]),
      .FROM_PART83(FROM_PART8[3]),
      .FROM_PART84(FROM_PART8[4]),
      .FROM_PART85(FROM_PART8[5]),
      .FROM_PART86(FROM_PART8[6]),
      .FROM_PART87(FROM_PART8[7]),
      .FROM_PART88(FROM_PART8[8]),
      .FROM_PART89(FROM_PART8[9]),
      .FROM_PART810(FROM_PART8[10])

    );


    initial begin

        $dumpfile("waveform/part123blob8.vcd");
        $dumpvars(0, part123blob8_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | enable=%b clk=%b BLOB0=%b BLOB1=%b BLOB2=%b BLOB3=%b ", $time, enable, i, FROM_BLOB[0], FROM_BLOB[1], FROM_BLOB[2], FROM_BLOB[3]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        rst_n = 0;
        enable = 0;
        I=1;
        #5000; rst_n = 1;
        #5000; enable = 1;

        for(i = 0; i < 130; i = i + 1)
        begin
          #5000; clk = ~clk;
          $display("Time=%0t | enable=%b clk=%b BLOB0=%b BLOB1=%b BLOB2=%b BLOB3=%b ", $time, enable, i, FROM_BLOB[0], FROM_BLOB[1], FROM_BLOB[2], FROM_BLOB[3]);
          #5000; clk = ~clk;
        end


        $finish; // End the simulation
    end

endmodule

