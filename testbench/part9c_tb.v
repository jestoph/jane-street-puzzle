`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part9c.v */
module part9c_tb;

    // Inputs
    reg [3:0] IN;

    // Outputs
    wire [15:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9c part9c_1 (
      //inputs
      .FROM_PART9A1(IN[3]),
      .FROM_PART9A2(IN[2]),
      .FROM_PART9A3(IN[1]),
      .FROM_PART9A4(IN[0]),
      //outputs
      .FROM_PART9C15(OUT[15]),
      .FROM_PART9C14(OUT[14]),
      .FROM_PART9C13(OUT[13]),
      .FROM_PART9C12(OUT[12]),
      .FROM_PART9C11(OUT[11]),
      .FROM_PART9C10(OUT[10]),
      .FROM_PART9C9(OUT[9]),
      .FROM_PART9C8(OUT[8]),
      .FROM_PART9C7(OUT[7]),
      .FROM_PART9C6(OUT[6]),
      .FROM_PART9C5(OUT[5]),
      .FROM_PART9C4(OUT[4]),
      .FROM_PART9C3(OUT[3]),
      .FROM_PART9C2(OUT[2]),
      .FROM_PART9C1(OUT[1]),
      .FROM_PART9C0(OUT[0])

    );

    initial begin

        $dumpfile("waveform/part9c.vcd");
        $dumpvars(0, part9c_tb);

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

