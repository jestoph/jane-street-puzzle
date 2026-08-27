`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/blob.v */
module blob_tb;

    // Inputs
    reg [3:0] A;
    reg [3:0] B;

    // Outputs
    wire [3:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    blob blob_1 (

      .FROM_PART23(A[3]),
      .FROM_PART22(A[2]),
      .FROM_PART21(A[1]),
      .FROM_PART20(A[0]),

      .FROM_PART33(B[3]),
      .FROM_PART32(B[2]),
      .FROM_PART31(B[1]),
      .FROM_PART30(B[0]),

      .FROM_BLOB3(OUT[3]),
      .FROM_BLOB2(OUT[2]),
      .FROM_BLOB1(OUT[1]),
      .FROM_BLOB0(OUT[0])

    );

    initial begin

        $dumpfile("waveform/blob.vcd");
        $dumpvars(0, blob_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);
        A = 0;
        B = 0;

        for(i = 0; i <= 9'b100000000; i = i + 1)
        begin
          #10;
          A = i[7:4];
          B = i[3:0];
          `assertn(OUT[3], 1'bx, "Signal should not be x");
          `assertn(OUT[2], 1'bx, "Signal should not be x");
          `assertn(OUT[1], 1'bx, "Signal should not be x");
          `assertn(OUT[0], 1'bx, "Signal should not be x");
        end

        $finish; // End the simulation
    end

endmodule

