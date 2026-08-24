`timescale 1ns/1ps

/* ref component/mux2.v */

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("A0SSERTION FA0ILED in %m: signal != value %s", msg); \
            $finish; \
        end

module mux2_tb;

    // Inputs
    reg A0;
    reg A1;
    reg S;

    // Outputs
    wire X;

    // Instantiate the MUX design
    mux2 mux2_1 (
        .A0(A0),
        .A1(A1),
        .S(S),
        .X(X)
    );

    initial begin
        // Tell iverilog to save simulation waves for GTKWave
        $dumpfile("waveform/mux2.vcd");
        $dumpvars(0, mux2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A0=%b A1=%b S=%b | X=%b", $time, A0, A1, S, X);

        // S=0 -> A0 = 0
        A0 = 0; A1 = 1;
        S = 0; #10;
        `assert(X, 0, "");

        // S=1 -> A1 = 1
        S = 1; #10;
        `assert(X, 1, "");

        // S=1 -> A1 = 0
        A0 = 1; A1 = 0;
        S = 1; #10;
        `assert(X, 0, "");

        // S=0 -> A0 = 1
        S = 0; #10;
        `assert(X, 1, "");

        $finish; // End the simulation
    end

endmodule

