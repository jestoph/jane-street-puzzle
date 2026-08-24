`timescale 1ns/1ps

/* ref component/and3.v */
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module and3_tb;

    // Inputs
    reg A;
    reg B;
    reg C;

    // Outputs
    wire X;

    // Instantiate the MUX design
    and3 and3_1 (
        .A(A),
        .B(B),
        .C(C),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/and3.vcd");
        $dumpvars(0, and3_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b C=%b | X=%b", $time, A, B, C, X);

        A = 0; B = 0; C = 0; #10;
        `assert(X, 0, "");
        A = 1; B = 0; C = 0; #10;
        `assert(X, 0, "");
        A = 0; B = 1; C = 0; #10;
        `assert(X, 0, "");
        A = 1; B = 1; C = 0; #10;
        `assert(X, 0, "");
        A = 0; B = 0; C = 1; #10;
        `assert(X, 0, "");
        A = 1; B = 0; C = 1; #10;
        `assert(X, 0, "");
        A = 0; B = 1; C = 1; #10;
        `assert(X, 0, "");
        A = 1; B = 1; C = 1; #10;
        `assert(X, 1, "");


        $finish; // End the simulation
    end

endmodule

