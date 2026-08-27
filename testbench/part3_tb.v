`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part3.v */
module part3_tb;

    // Inputs
    reg S;
    reg A;
    reg rst_n;
    reg clk;

    // Outputs
    // These are always opposite when A=1
    // Otherwise, S is low and Q is just latched to whatever it was
    wire [4:0] O;

    integer i; // 32 bit

    part3 part3_1 (
      // inputs
      .rst_n(rst_n),
      .clk(clk),
      .FROM_PART24(A),
      .S(S),
      // outputs
      .FROM_PART34(O[4]),
      .FROM_PART33(O[3]),
      .FROM_PART32(O[2]),
      .FROM_PART31(O[1]),
      .FROM_PART30(O[0])
    );

    initial begin

        $dumpfile("waveform/part3.vcd");
        $dumpvars(0, part3_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, enable, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S = 0; A = 0;
        rst_n = 0;
        #5000; clk = ~clk;
        #5000; rst_n = 1;

        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end
        S = 0; A = 1;
        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end
        S = 1; A = 0;
        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end
        S = 1; A = 1;
        for(i = 0; i < 130 ; i = i + 1)
        begin
          #5000; clk = ~clk;
        end


        $finish; // End the simulation
    end

endmodule

