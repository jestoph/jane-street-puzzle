`timescale 1ns/1ps

/* ref component/nand2.v */

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module nand2_tb;

    // Inputs
    reg A;
    reg B;

    // Outputs
    wire Y;

    // Instantiate the MUX design
    nand2 nand2_1 (
        .A(A),
        .B(B),
        .Y(Y)
    );

    initial begin

        $dumpfile("waveform/nand2.vcd");
        $dumpvars(0, nand2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b | Y=%b", $time, A, B, Y);

        A = 0; B = 0; #10;
        `assert(Y, 1, "");

        A = 1; B = 0; #10;
        `assert(Y, 1, "");

        A = 0; B = 1; #10;
        `assert(Y, 1, "");

        A = 1; B = 1; #10;
        `assert(Y, 0, "");

        $finish; // End the simulation
    end

endmodule

