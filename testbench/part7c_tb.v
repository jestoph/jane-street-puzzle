`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part7c.v */
module part7c_tb;

    // Inputs
    reg I;
    reg clk;
    reg S;
    reg rst_n;
    reg A;

    // Outputs
    wire O;

    integer i; // 32 bit

    part7c part7c_1 (
      // Inputs
      .I(I),
      .S(S),
      .rst_n(rst_n),
      .clk(clk),
      .FROM_PART7B0(A),
      // Outputs
      .FROM_PART7C0(O)
    );

    initial begin

        $dumpfile("waveform/part7c.vcd");
        $dumpvars(0, part7c_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S = 0;
        I = 0;
        rst_n = 0;
        #5000; rst_n = 1;
        #5000; S = 1;

        for( i = 0; i < 5'b100; i = i + 1)
        begin

          #5000; A = i[0];
          #5000; I = i[1];
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;

        end

        #5000; rst_n = ~rst_n;
        #5000; rst_n = ~rst_n;

        for( i = 0; i < 5'b100; i = i + 1)
        begin

          #5000; A = i[0];
          #5000; I = i[1];
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000; clk = ~clk;

        end

        $finish; // End the simulation
    end

endmodule

