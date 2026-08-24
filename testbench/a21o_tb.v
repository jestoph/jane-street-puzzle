`timescale 1ns/1ps

/* ref component/a21o.v */
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module a21o_tb;

    // Inputs
    reg A1;
    reg A2;
    reg B1;

    // Outputs
    wire X;

    // Instantiate the MUX design
    a21o a21o_1 (
        .A1(A1),
        .A2(A2),
        .B1(B1),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/a21o.vcd");
        $dumpvars(0, a21o_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A1=%b A2=%b B1=%b | X=%b", $time, A1, A2, B1, X);

        A1 = 0; A2 = 0; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 0; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 1; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 1; B1 = 0; #10;
        `assert(X, 1, "");
        A1 = 0; A2 = 0; B1 = 1; #10;
        `assert(X, 1, "");
        A1 = 1; A2 = 0; B1 = 1; #10;
        `assert(X, 1, "");
        A1 = 0; A2 = 1; B1 = 1; #10;
        `assert(X, 1, "");
        A1 = 1; A2 = 1; B1 = 1; #10;
        `assert(X, 1, "");


        $finish; // End the simulation
    end

endmodule

