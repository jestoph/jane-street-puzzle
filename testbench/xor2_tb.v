`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref component/xor2.v */
module xor2_tb;

    // Inputs
    reg A;
    reg B;

    // Outputs
    wire X;

    // Instantiate the MUX design
    xor2 xor2_1 (
        .A(A),
        .B(B),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/xor.vcd");
        $dumpvars(0, xor2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b | X=%b", $time, A, B, X);

        A = 0; B = 0; #10;
        `assert(X, 0, "");

        A = 1; B = 0; #10;
        `assert(X, 1, "");

        A = 0; B = 1; #10;
        `assert(X, 1, "");

        A = 1; B = 1; #10;
        `assert(X, 0, "");

        $finish; // End the simulation
    end

endmodule

