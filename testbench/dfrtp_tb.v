`timescale 1ns/1ps

/* ref component/dfrtp.v */

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

`define assertn(signal, value, msg) \
        if (signal === value) begin \
            $display("ASSERTION FAILED in %m: signal == value %s", msg); \
            $finish; \
        end

module dfrtp_tb;

    // Inputs
    reg D;
    reg CLK;
    reg RESET_B;

    // Outputs
    output wire Q;

    // Instantiate the MUX design
    dfrtp dfrtp_1 (
        .D(D),
        .CLK(CLK),
        .RESET_B(RESET_B),
        .Q(Q)
    );

    initial begin

        $dumpfile("waveform/dfrtp.vcd");
        $dumpvars(0, dfrtp_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | D=%b CLK=%b RESET_B=%b | Q=%b", $time, D, CLK, RESET_B, Q);

        D = 0; CLK = 1;
        `assertn(Q, 0, "");
        `assertn(Q, 1, "");
        #10;
        `assert(Q, 0, "");

        D = 1; CLK = 0; #10;
        `assert(Q, 0, "");

        D = 1; CLK = 1; #10;
        `assert(Q, 1, "");

        D = 0; CLK = 1; #10;
        `assert(Q, 1, "");

        $finish; // End the simulation
    end

endmodule

