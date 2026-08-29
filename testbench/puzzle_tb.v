`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/puzzle.v */
module puzzle_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg enable;

    // Outputs
    wire success;
    // wire flag;

    wire [7:0] O;


    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned


    puzzle puzzle_1 (

      .I(I),
      .clk(clk),
      .enable(enable),
      .rst_n(rst_n),

      .success(success),

      .O0(O[0]),
      .O1(O[1]),
      .O2(O[2]),
      .O3(O[3]),
      .O4(O[4]),
      .O5(O[5]),
      .O6(O[6]),
      .O7(O[7])

    );

    initial begin

        $dumpfile("waveform/puzzle.vcd");
        $dumpvars(0, puzzle_tb);

        // Track changes directly in the terminal window
        /*
        $monitor("Time=%0t | I=%b clk=%b enable=%b rst_n=%b | success=%b O[0]=%b Wire_3=%b Wire_488=%b",
          $time,
          I,
          clk,
          enable,
          rst_n,
          success,
          O0,
          puzzle_1.Wire_3,
          puzzle_1.Wire_488,
        );
        */


        I = 0;
        enable = 0;
        rst_n = 0;
        clk = 0;

        #5000; rst_n = 1;

        #5000; clk = ~clk; #5000; clk = ~clk;
        #5000; clk = ~clk; #5000; clk = ~clk;
        #5000; clk = ~clk; #5000; clk = ~clk;
        #5000; clk = ~clk; #5000; clk = ~clk;

        enable = 1;



        for( i = 0 ; i < 121 ; i = i + 1)
        begin
          //I = 1'(i);
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end

        enable = 0;

        for( i = 0 ; i < 140 ; i = i + 1)
        begin
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end





        $finish; // End the simulation
    end

endmodule

