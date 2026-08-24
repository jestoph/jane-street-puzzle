`timescale 1ns/1ps

/* ref component/a21boi.v */
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module a21boi_tb;

    // Inputs
    reg A1;
    reg A2;
    reg B1_N;

    // Outputs
    wire Y;

    // Instantiate the MUY design
    a21boi a21boi_1 (
        .A1(A1),
        .A2(A2),
        .B1_N(B1_N),
        .Y(Y)
    );

    initial begin

        $dumpfile("waveform/a21boi.vcd");
        $dumpvars(0, a21boi_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A1=%b A2=%b B1_N=%b | Y=%b", $time, A1, A2, B1_N, Y);

        A1 = 0; A2 = 0; B1_N = 0; #10;
        `assert(Y, 0, "");
        A1 = 1; A2 = 0; B1_N = 0; #10;
        `assert(Y, 0, "");
        A1 = 0; A2 = 1; B1_N = 0; #10;
        `assert(Y, 0, "");
        A1 = 1; A2 = 1; B1_N = 0; #10;
        `assert(Y, 0, "");
        A1 = 0; A2 = 0; B1_N = 1; #10;
        `assert(Y, 0, "");
        A1 = 1; A2 = 0; B1_N = 1; #10;
        `assert(Y, 0, "");
        A1 = 0; A2 = 1; B1_N = 1; #10;
        `assert(Y, 0, "");
        A1 = 1; A2 = 1; B1_N = 1; #10;
        `assert(Y, 0, "");


        $finish; // End the simulation
    end

endmodule

