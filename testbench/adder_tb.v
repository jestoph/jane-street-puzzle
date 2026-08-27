`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/adder.v */
module adder_tb;

    // Inputs
    reg [7:0] A;
    reg [7:0] B;

    reg [8:0] tmp;

    // Outputs
    wire [8:0] X;

    integer i; // 32 bit

    adder adder_1 (

      /* input A from sr1 */
      /* ref testbench/sr1_tb.v */
      .Wire_9 (A[7]),
      .Wire_23(A[6]),
      .Wire_1 (A[5]),
      .Wire_31(A[4]),
      .Wire_12(A[3]),
      .Wire_14(A[2]),
      .Wire_10(A[1]),
      .Wire_13(A[0]),

      /* input B from sr2 */
      /* ref testbench/sr2_tb.v */
      .Wire_20(B[7]),
      .Wire_27(B[6]),
      .Wire_28(B[5]),
      .Wire_26(B[4]),
      .Wire_19(B[3]),
      .Wire_29(B[2]),
      .Wire_24(B[1]),
      .Wire_25(B[0]),

      /* outputs */
      .Wire_2  (X[8]), // Why is this guy 1? How/Why did I guess that this was the 9th bit?

      /* This set works for B=0 */
      /* ref testbench/comparitor_tb.v */
      .Wire_69 (X[7]),
      .Wire_68 (X[6]),
      .Wire_102(X[5]),
      .Wire_111(X[4]),
      .Wire_101(X[3]),
      .Wire_100(X[2]),
      .Wire_109(X[1]),
      .Wire_96 (X[0])

    );

    initial begin

        $dumpfile("waveform/adder.vcd");
        $dumpvars(0, adder_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        A = 8'b0;
        B = 8'b0;
        #10;

        for (i = 8'b10000000 ; i > 0; i = (i >> 1) & 8'b11111111)
        begin
            B = i;
            #10;
            `assert(X[8], 0, "When A is zero, the top bit of the output should be 0");
            `assert(X[7:0], B, "When A is zero, the output should equal B");
        end

        A = 8'b0;
        B = 8'b0;
        #10;

        for (i = 8'b00000001 ; i > 0; i = (i << 1) & 8'b11111111)
        begin
            A = i;
            #10;
            `assert(X[8], 0, "When A is zero, the top bit of the output should be 0");
            `assert(X[7:0], A, "When B is zero, the output should equal A");
        end

        /****************************
        * SUM AGAINST 0
        *****************************/

        /* When B is zero, the output should be A */
        A = 8'b0;
        B = 8'b0;
        #10;

        for (i = 0; i < 8'b11111111; i = i + 1)
        begin
            A = i;
            #10;
            `assert(X[8], 0, "When B is zero, the top bit of the output should be 0");
            `assert(X[7:0], A, "When B is zero, the output should equal A");
        end

        /* When B is zero, the output should be A */
        A = 8'b0;
        B = 8'b0;
        #10;

        for (i = 0; i < 8'b11111111; i = i + 1)
        begin
            B = i;
            #10;
            `assert(X[8], 0, "When B is zero, the top bit of the output should be 0");
            `assert(X[7:0], B, "When A is zero, the output should equal B");
        end


        /****************************
        * SUM
        *****************************/
        A = 8'b0;
        B = 8'b0;
        #10;

        for (i = 0; i < 8'b11111111; i = i + 1)
        begin
            A = i;
            B = i;
            tmp = (i + i);
            #10;
            `assert(X, tmp, "X = A + B");
        end

        A = 8'b11111000;
        B = 8'b11111000;
        #10
        `assert(X, 9'b111110000, "Result");



        $finish; // End the simulation
    end

endmodule

