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
    wire Y;

    // Instantiate the MUX design
    and3 and3_1 (
        .A(A),
        .B(B),
        .C(C),
        .Y(Y)
    );

    initial begin

        $dumpfile("waveform/and3.vcd");
        $dumpvars(0, and3_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b C=%b | Y=%b", $time, A, B, C, Y);

        A = 0; B = 0; C = 0; #10;
        A = 1; B = 0; C = 0; #10;
        A = 0; B = 1; C = 0; #10;
        A = 1; B = 1; C = 0; #10;
        A = 0; B = 0; C = 1; #10;
        A = 1; B = 0; C = 1; #10;
        A = 0; B = 1; C = 1; #10;
        A = 1; B = 1; C = 1; #10;


        $finish; // End the simulation
    end

endmodule

