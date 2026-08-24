`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

/* ref outputs/sr1.v */
module sr1_tb;

    // Inputs
    reg IN;
    reg RESET_B;
    reg CLK;
    reg EN;

    // Outputs
    wire [7:0] X;


    sr1 sr1_1 (
      /* inputs */
      .Wire_8(EN),
      .Wire_9(IN),
      .Wire_3(CLK),
      .Wire_11(RESET_B),

      /* output */
      .Wire_18(X[0]),
      .Wire_75(X[1]),
      .Wire_78(X[2]),
      .Wire_16(X[3]),
      .Wire_76(X[4]),
      .Wire_19(X[5]),
      .Wire_6(X[6]),
      .Wire_17(X[7])
    );

    initial begin

        $dumpfile("waveform/sr1.vcd");
        $dumpvars(0, sr1_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | IN=%b RESET_B=%b EN=%b CLK=%b | X=%b", $time, IN, RESET_B, EN, CLK, X);

        EN  = 1'b0 ; #10;

        $finish; // End the simulation
    end

endmodule

