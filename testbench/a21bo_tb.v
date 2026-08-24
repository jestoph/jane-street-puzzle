`timescale 1ns/1ps

/* ref component/a21bo.v */
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module a21bo_tb;

    // Inputs
    reg A1;
    reg A2;
    reg B1_N;

    // Outputs
    wire X;

    // Instantiate the MUX design
    a21bo a21bo_1 (
        .A1(A1),
        .A2(A2),
        .B1_N(B1_N),
        .X(X)
    );

    initial begin

        $dumpfile("waveform/a21bo.vcd");
        $dumpvars(0, a21bo_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A1=%b A2=%b B1_N=%b | X=%b", $time, A1, A2, B1_N, X);

        // TODO: Not sure the correct behaviour
        A1 = 0; A2 = 0; B1_N = 0; #10;
        //`assert(X, 0, "");
        A1 = 1; A2 = 0; B1_N = 0; #10;
        //`assert(X, 0, "");
        A1 = 0; A2 = 1; B1_N = 0; #10;
        //`assert(X, 0, "");
        A1 = 1; A2 = 1; B1_N = 0; #10;
        //`assert(X, 0, "");
        A1 = 0; A2 = 0; B1_N = 1; #10;
        //`assert(X, 0, "");
        A1 = 1; A2 = 0; B1_N = 1; #10;
        //`assert(X, 0, "");
        A1 = 0; A2 = 1; B1_N = 1; #10;
        //`assert(X, 0, "");
        A1 = 1; A2 = 1; B1_N = 1; #10;
        //`assert(X, 0, "");


        $finish; // End the simulation
    end

endmodule

