`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

module sr2_tb;

    // Inputs
    reg IN;
    reg RESET_B;
    reg CLK;
    reg EN;

    // Outputs
    wire [7:0] X;


    sr2 sr2_1 (
      /* inputs */
      .Wire_8(EN),
      .Wire_21(IN),
      .Wire_34(CLK),
      .Wire_11(RESET_B),

      /* output */
      .Wire_23(X[0]),
      .Wire_80(X[1]),
      .Wire_74(X[2]),
      .Wire_73(X[3]),
      .Wire_81(X[4]),
      .Wire_79(X[5]),
      .Wire_22(X[6]),
      .Wire_77(X[7])
    );

    initial begin

        $dumpfile("waveform/sr2.vcd");
        $dumpvars(0, sr2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | IN=%b RESET_B=%b EN=%b CLK=%b | X=%b", $time, IN, RESET_B, EN, CLK, X);

        EN  = 1'b0 ; #10;

        $finish; // End the simulation
    end

endmodule

