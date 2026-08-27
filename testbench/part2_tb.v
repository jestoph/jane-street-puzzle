`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal (%b) != value (%b) %s", signal, value, msg); \
            $finish; \
        end

/* ref outputs/part2.v */
module part2_tb;

    // Inputs
    reg rst_n;
    reg clk;
    reg S;

    wire [3:0] O;
    wire O1;
    wire O2;
    wire O3;
    wire O4;
    wire O5;

    integer i; // 32 bit

    part2 part2_1 (
      .rst_n(rst_n),
      .clk(clk),
      .S(S),
      .Wire_130(O[3]),
      .Wire_110(O[2]),
      .Wire_80 (O[1]),
      .Wire_79 (O[0])
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

