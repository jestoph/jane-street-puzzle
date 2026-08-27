`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal (%b) != value (%b) %s", signal, value, msg); \
            $finish; \
        end

/* ref outputs/part1.v */
module part1_tb;

    // Inputs
    reg A;
    reg B;
    reg rst_n;
    reg clk;
    reg enable;

    // Outputs
    // These are always opposite when enable=1
    // Otherwise, S is low and Q is just latched to whatever it was
    wire Q;
    wire S;

    integer i; // 32 bit

    part1 part1_1 (
      .rst_n(rst_n),
      .clk(clk),
      .enable(enable),
      .Wire_394(A),
      .Wire_427(B),
      .TO_OUTPUT0(Q),
      .S(S)
    );

    initial begin

        $dumpfile("waveform/part1.vcd");
        $dumpvars(0, part1_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        A = 0; B = 0;
        enable = 0;
        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; enable = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 0, "When starting up should be 0 I think");
        `assert(S, 1, "When starting up should be 1 I think");

        #5000; A = 0; B = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 0, "Need A & B to be high");
        `assert(S, 1, "When starting up should be 1 I think");

        #5000; A = 1; B = 0;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 0, "Need A & B to be high");
        `assert(S, 1, "When starting up should be 1 I think");

        #5000; A = 1; B = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 1, "What A=1 & B=1 we latch in 1")
        `assert(S, 0, "When starting up should be 1 I think");

        #5000; A = 1; B = 0;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 1, "Should latch in high value");
        `assert(S, 0, "When starting up should be 1 I think");

        #5000; A = 0; B = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 1, "Should latch in high value");
        `assert(S, 0, "When starting up should be 1 I think");

        #5000; A = 0; B = 0;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 1, "Should latch in high value");
        `assert(S, 0, "When starting up should be 1 I think");

        #5000; rst_n = 0;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        #5000; rst_n = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        #3000; enable = 0;
        #5000; clk = ~clk;
        `assert(S, 0, "When starting up should be 1 I think");
        #5000; clk = ~clk;

        #5000; A = 1; B = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 0, "No latching behaviour when en=0")
        `assert(S, 0, "When starting up should be 1 I think");
        #3000; enable = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(Q, 1, "Latching works when en=1")


        $finish; // End the simulation
    end

endmodule

