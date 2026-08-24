`timescale 1ns/1ps

/* ref component/a31o.v */
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module a31o_tb;

    // Inputs
    reg A1;
    reg A2;
    reg A3;
    reg B1;

    // Outputs
    wire X;

    // Instantiate the MUX design
    a31o a31o_1 (
        .A1(A1),
        .A2(A2),
        .A3(A3),
        .B1(B1),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/a31o.vcd");
        $dumpvars(0, a31o_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A1=%b A2=%b A3=%b B1=%b | X=%b", $time, A1, A2, A3, B1, X);

        A1 = 0; A2 = 0; A3 = 0; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 0; A3 = 0; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 1; A3 = 0; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 1; A3 = 0; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 0; A3 = 1; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 0; A3 = 1; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 1; A3 = 1; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 1; A3 = 1; B1 = 0; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 0; A3 = 0; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 0; A3 = 0; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 1; A3 = 0; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 1; A3 = 0; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 0; A3 = 1; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 0; A3 = 1; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 0; A2 = 1; A3 = 1; B1 = 1; #10;
        `assert(X, 0, "");
        A1 = 1; A2 = 1; A3 = 1; B1 = 1; #10;
        `assert(X, 0, "");


        $finish; // End the simulation
    end

endmodule

