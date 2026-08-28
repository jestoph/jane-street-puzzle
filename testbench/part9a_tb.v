`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part9a.v */
module part9a_tb;

    // Inputs
    reg success;
    reg clk;
    reg [11:0] IN;

    // Outputs
    wire [7:0] OUT;
    wire [3:0] W_OUT;
    wire [3:0] W2_OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9a part9a_1 (
      // inputs
      .success(success),
      .clk(clk),

      .FROM_PART9B0(IN[0]),
      .FROM_PART9B1(IN[1]),
      .FROM_PART9B2(IN[2]),
      .FROM_PART9B3(IN[3]),
      .FROM_PART9B4(IN[4]),
      .FROM_PART9B5(IN[5]),
      .FROM_PART9B6(IN[6]),
      .FROM_PART9B7(IN[7]),
      .MSG0        (IN[8]),
      .MSG1        (IN[9]),
      .MSG2        (IN[10]),
      .MSG3        (IN[11]),

      // outputs
      .O7(OUT[7]),
      .O5(OUT[6]),
      .O4(OUT[5]),
      .O3(OUT[4]),
      .O6(OUT[3]),
      .O1(OUT[2]),
      .O2(OUT[1]),
      .O0(OUT[0]),
      .FROM_PART9A1(W2_OUT[3]),
      .FROM_PART9A2(W2_OUT[2]),
      .FROM_PART9A3(W2_OUT[1]),
      .FROM_PART9A4(W2_OUT[0]),
      .FROM_PART9A5(W_OUT[3]),
      .FROM_PART9A6(W_OUT[2]),
      .FROM_PART9A7(W_OUT[1]),
      .FROM_PART9A8(W_OUT[0])

    );

    initial begin

        $dumpfile("waveform/part9a.vcd");
        $dumpvars(0, part9a_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);

        clk = 0;
        IN = 0;
        success = 0;
        for(i = 0; i <= 12'b100000000000; i = i + 1)
        begin
          #10 IN = 12'(i);
          #10;
          #10; clk = ~clk;
          #10;
          #10; clk = ~clk;
        end

        #10; clk = ~clk;
        #10; clk = ~clk;
        #10; clk = ~clk;
        #10; clk = ~clk;
        #10; clk = ~clk;

        success = 1;
        for(i = 0; i <= 12'b100000000000; i = i + 1)
        begin
          #10 IN = 12'(i);
          #10;
          #10; clk = ~clk;
          #10;
          #10; clk = ~clk;
        end

        $finish; // End the simulation
    end

endmodule

