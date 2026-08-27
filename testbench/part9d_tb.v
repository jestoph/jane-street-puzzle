`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part9d.v */
module part9d_tb;

    // Inputs
    reg [3:0] IN;

    // Outputs
    wire [7:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9d part9d_1 (

      //inputs
      .OB4(IN[3]),
      .OB3(IN[2]),
      .OB2(IN[1]),
      .OB1(IN[0]),

      //outputs
      .FROM_PART9D7(OUT[7]),
      .FROM_PART9D6(OUT[6]),
      .FROM_PART9D5(OUT[5]),
      .FROM_PART9D4(OUT[4]),
      .FROM_PART9D3(OUT[3]),
      .FROM_PART9D2(OUT[2]),
      .FROM_PART9D1(OUT[1]),
      .FROM_PART9D0(OUT[0])

    );

    initial begin

        $dumpfile("waveform/part9d.vcd");
        $dumpvars(0, part9d_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);

        IN = 0;
        for(i = 0; i <= 5'b10000; i = i + 1)
        begin
          IN = i;
          #10;
        end

        $finish; // End the simulation
    end

endmodule

