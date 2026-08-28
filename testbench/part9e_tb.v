`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part9e.v */
module part9e_tb;

    // Inputs
    reg [3:0] IN;

    // Outputs
    wire [7:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9e part9e_1 (
      //inputs
      .FROM_PART9A1(IN[3]),
      .FROM_PART9A2(IN[2]),
      .FROM_PART9A3(IN[1]),
      .FROM_PART9A4(IN[0]),

      //outputs
      .FROM_PART9E7(OUT[7]),
      .FROM_PART9E6(OUT[6]),
      .FROM_PART9E5(OUT[5]),
      .FROM_PART9E4(OUT[4]),
      .FROM_PART9E3(OUT[3]),
      .FROM_PART9E2(OUT[2]),
      .FROM_PART9E1(OUT[1]),
      .FROM_PART9E0(OUT[0])
    );

    initial begin

        $dumpfile("waveform/part9e.vcd");
        $dumpvars(0, part9e_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);

        IN = 0;
        for(i = 0; i <= 5'b10000; i = i + 1)
        begin
          IN = 4'(i);
          #10;
        end

        $finish; // End the simulation
    end

endmodule

