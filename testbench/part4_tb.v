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

        /* When A is zero, the output should be B */
        clk = 0;
        S = 1'b1; //1;      // S seems to have no impact?
        I = 1'b1;
        rst_n = 0;
        /*
        * Part5 seems to only have three patterns -
        *  - 3'b011
        *  - 3'b101
        *  - 3'b111
        *  */
        FROM_PART5 = 0;
        FROM_PART7A = 0;
        FROM_PART7B = 0;
        FROM_PART7C = 0;

        #5000; rst_n = ~rst_n;


        /***** BEHAVIOUR ONE: TO_OUTPUT1 depends on all part7 being high ******/

        /* When all from 7 are high, TO_OUTPUT1 is high */
        FROM_PART7A = 7;
        FROM_PART7B = 7'h7f;
        FROM_PART7C = 1;

        #5000;

        `assert(TO_OUTPUT1, 1, "Should be high with this pattern");
        #5000;
        FROM_PART7C = 0;
        #5000;
        `assert(TO_OUTPUT1, 0, "Should be low now");


        #5000; rst_n = ~rst_n;
        #5000; rst_n = ~rst_n;

        /***** BEHAVIOUR TWO: TO_OUTPUT2 latches low after interaction with SR
        * values ******/

        `assert(TO_OUTPUT2, 1, "OUTPUT2 starts high after reset");
        FROM_PART5  = 3'b111;
        #5000; I=1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(TO_OUTPUT2, 1, "OUTPUT2 starts high after reset");
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(TO_OUTPUT2, 0, "SR0 should be high now which should cascade to OUTPUT2 being low");


        #5000; rst_n = ~rst_n;
        #5000; rst_n = ~rst_n;
        #5000; I=1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(part4_1.SR0, 1, "Should have shifted in");
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(part4_1.SR1, 1, "Should have shifted in");
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(part4_1.SR2, 1, "Should have shifted in");
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(part4_1.SR3, 1, "Should have shifted in");
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(part4_1.SR4, 1, "Should have shifted in");
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(part4_1.SR5, 1, "Should have shifted in");




        $finish; // End the simulation
    end

endmodule

