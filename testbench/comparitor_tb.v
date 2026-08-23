`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module comparitor_tb;

    // Inputs
    reg [8:0] I;

    // Outputs
    wire X;

    // Instantiate the MUX design
    // module comparitor(
    //   input wire Wire_114,
    //   input wire Wire_103,
    //   input wire Wire_72,
    //   input wire Wire_2,
    //   input wire Wire_99,
    //   input wire Wire_112,
    //   input wire Wire_71,
    //   input wire Wire_104,
    //   input wire Wire_105,
    //   output wire Wire_36
    // );

    comparitor comparitor_1 (
      .Wire_114(I[0]),
      .Wire_103(I[1]),
      .Wire_72(I[2]),
      .Wire_2(I[3]),
      .Wire_99(I[4]),
      .Wire_112(I[5]),
      .Wire_71(I[6]),
      .Wire_104(I[7]),
      .Wire_105(I[8]),

      .Wire_36(X)
    );

    initial begin

        $dumpfile("waveform/comparitor.vcd");
        $dumpvars(0, comparitor_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | I=%b | X=%b", $time, I, X);

        I = 9'b111111111 ; #10;

        I = 1; #10;

        I = 1; #10;

        I = 0; #10;

        $finish; // End the simulation
    end

endmodule

