`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part9.v */
module part9_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;      // I think I and S are opposite once puzzle locks?
    reg success;

    reg [3:0] MSG;

    // Outputs
    wire [7:0] OUTPUT;

    integer i; // 32 bit
    integer j; // 32 bit


    part9 part9_1 (

      // inputs
      .I(I),
      .S(S),
      .clk(clk),
      .rst_n(rst_n),
      .success(success),

      // outputs
      .MSG0(MSG[0]),
      .MSG1(MSG[1]),
      .MSG2(MSG[2]),
      .MSG3(MSG[3]),

      .O0(OUTPUT[0]),
      .O1(OUTPUT[1]),
      .O2(OUTPUT[2]),
      .O3(OUTPUT[3]),
      .O4(OUTPUT[4]),
      .O5(OUTPUT[5]),
      .O6(OUTPUT[6]),
      .O7(OUTPUT[7])


    );

    initial begin

        $dumpfile("waveform/part9.vcd");
        $dumpvars(0, part9_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S=1; I=1; // try all combos
        rst_n = 0;
        success = 0;
        #5000; rst_n = 1;
        // #5000; S=0; I=0; // gives - e8e31774fae390a82ea9d494bcef8d
        // #5000; S=0; I=1; // gives - e8e31774fae390a82ea9d494bcef8d
        // #5000; S=1; I=0; // gives - e8e76ea947d04f1237fefc1f7d2834
        // #5000; S=1; I=1; // gives - e8e66dae48ce7268c3162cbe3eaf3a
        #5000; success = 0;





        for( j = 0 ; j < 5'b10000 ; j = j + 1 )
        begin
          #5000; rst_n = ~rst_n;
          #5000; rst_n = ~rst_n;
          #5000; MSG = 4'(j); // try all 16 combos


          for( i = 0 ; i < 100; i = i + 1 )
          begin
            #5000; clk = ~clk;
            #5000; clk = ~clk;

          end


        end


        $finish; // End the simulation
    end

endmodule

