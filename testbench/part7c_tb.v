`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part7c.v */
module part7c_tb;

    // Inputs
    reg I;
    reg clk;
    reg S;
    reg rst_n;
    reg FROM_PART7B0;

    // Outputs
    wire FROM_PART7C0;

    integer i; // 32 bit
    integer j; // 32 bit

    part7c part7c_1 (
      // Inputs
      .I(I),
      .S(S),
      .rst_n(rst_n),
      .clk(clk),
      .FROM_PART7B0(FROM_PART7B0),
      // Outputs
      .FROM_PART7C0(FROM_PART7C0)
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
        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; S = 1;

        for (j = 0 ; j < 1<<12; j = j + 1)
        begin
          #5000; rst_n = 0;
          #5000; rst_n = 1;
          FROM_PART7B0 = 1;

          for( i = 0; i < 11; i = i + 1)
          begin

            #5000;
            FROM_PART7B0 = 0;
            I = 0;
            if(i==0)
            begin
              FROM_PART7B0 = 1;
            end

            if( (32'(1<<i) & j) != 0)
            begin
              I=1;
            end

            #5000; clk = ~clk;
            #5000; clk = ~clk;

          end
          FROM_PART7B0 = 0;

        end

        for( i = 0; i < 11; i = i + 1)
        begin

          #5000;
          FROM_PART7B0 = 0;
          I=1;
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end


        $finish; // End the simulation
    end

endmodule

