`timescale 1ns/1ps

/* ref component/and2.v */
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module and2_tb;

    // Inputs
    reg A;
    reg B;

    // Outputs
    wire X;

    // Instantiate the MUX design
    and2 and2_1 (
        .A(A),
        .B(B),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/and2.vcd");
        $dumpvars(0, and2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b | X=%b", $time, A, B, X);

        A = 0; B = 1; #10;
        `assert(X, 0, "");

        A = 1; B = 0; #10;
        `assert(X, 0, "");

        A = 0; B = 0; #10;
        `assert(X, 0, "");

        A = 1; B = 1; #10;
        `assert(X, 1, "");

        $finish; // End the simulation
    end

endmodule

