`timescale 1ns/1ps

/* ref component/mux2.v */

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module mux2_tb;

    // Inputs
    reg A;
    reg B;
    reg S;

    // Outputs
    wire Y;

    // Instantiate the MUX design
    mux2 mux2_1 (
        .A(A),
        .B(B),
        .S(S),
        .Y(Y)
    );

    initial begin
        // Tell iverilog to save simulation waves for GTKWave
        $dumpfile("waveform/mux2.vcd");
        $dumpvars(0, mux2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b S=%b | Y=%b", $time, A, B, S, Y);

        // Test Case 1: S=0 -> 0
        A = 0; B = 1; S = 0; #10;

        // Test Case 2: S=0 -> 1
        A = 1; B = 0; S = 0; #10;

        // Test Case 3: S=1 -> 0
        A = 1; B = 0; S = 1; #10;

        // Test Case 4: S=1 -> 1
        A = 0; B = 1; S = 1; #10;

        $finish; // End the simulation
    end

endmodule

