`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part4.v */
module part4_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [2:0] FROM_PART5;
    reg [2:0] FROM_PART7A;
    reg [6:0] FROM_PART7B;
    reg FROM_PART7C;

    // Outputs
    wire TO_OUTPUT1;
    wire TO_OUTPUT2;

    integer i; // 32 bit
    integer j; // 32 bit

    part4 part4_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART7B7(FROM_PART7B[6]),
      .FROM_PART7B6(FROM_PART7B[5]),
      .FROM_PART7B5(FROM_PART7B[4]),
      .FROM_PART7B4(FROM_PART7B[3]),
      .FROM_PART7B3(FROM_PART7B[2]),
      .FROM_PART7B2(FROM_PART7B[1]),
      .FROM_PART7B1(FROM_PART7B[0]),

      .FROM_PART7C0(FROM_PART7C),

      .FROM_PART52(FROM_PART5[2]),
      .FROM_PART51(FROM_PART5[1]),
      .FROM_PART50(FROM_PART5[0]),

      .FROM_PART7A2(FROM_PART7A[2]),
      .FROM_PART7A1(FROM_PART7A[1]),
      .FROM_PART7A0(FROM_PART7A[0]),

      // outputs
      .TO_OUTPUT1(TO_OUTPUT1),
      .TO_OUTPUT2(TO_OUTPUT2)
    );

    initial begin

        $dumpfile("waveform/part4.vcd");
        $dumpvars(0, part4_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S = 1'bx; //1;      // S seems to have no impact?
        I = 1'bx;
        rst_n = 0;

        #5000; rst_n = 1;

        FROM_PART5  = 3'bx;
        FROM_PART7A = 7;
        FROM_PART7B = 7'h7f;
        FROM_PART7C = 1;

        #5000;

        `assert(TO_OUTPUT1, 1, "Should be high with this pattern")
        `assert(TO_OUTPUT2, 1, "Should be high with this pattern")



        $finish; // End the simulation
    end

endmodule

