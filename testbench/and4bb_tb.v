`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref component/and4bb.v */
module and4bb_tb;

    // Inputs
    reg A_N;
    reg B_N;
    reg C;
    reg D;

    // Outputs
    wire X;

    // Instantiate the MUX design
    and4bb and4bb_1 (
        .A_N(A_N),
        .B_N(B_N),
        .C(C),
        .D(D),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/and4bb.vcd");
        $dumpvars(0, and4bb_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A_N=%b B_N=%b C=%b D=%b| X=%b", $time, A_N, B_N, C, D, X);

        A_N = 0; B_N = 0; C = 0; D = 0; #10;
        //`assert(X, 0, "");
        A_N = 1; B_N = 0; C = 0; D = 0; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 1; C = 0; D = 0; #10;
        `assert(X, 0, "");
        A_N = 1; B_N = 1; C = 0; D = 0; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 0; C = 1; D = 0; #10;
        `assert(X, 0, "");
        A_N = 1; B_N = 0; C = 1; D = 0; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 1; C = 1; D = 0; #10;
        `assert(X, 0, "");
        A_N = 1; B_N = 1; C = 1; D = 0; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 0; C = 0; D = 1; #10;
        `assert(X, 0, "");
        A_N = 1; B_N = 0; C = 0; D = 1; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 1; C = 0; D = 1; #10;
        `assert(X, 0, "");
        A_N = 1; B_N = 1; C = 0; D = 1; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 0; C = 1; D = 1; #10;
        `assert(X, 1, "");
        A_N = 1; B_N = 0; C = 1; D = 1; #10;
        `assert(X, 0, "");
        A_N = 0; B_N = 1; C = 1; D = 1; #10;
        `assert(X, 0, "");
        A_N = 1; B_N = 1; C = 1; D = 1; #10;
        `assert(X, 0, "");


        $finish; // End the simulation
    end

endmodule

