`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/sr2.v */
module sr2_tb;

    // Inputs
    reg IN;
    reg RESET_B;
    reg CLK;
    reg EN;

    // Outputs
    wire [7:0] X;

    integer i;

    sr2 sr2_1 (
      /* inputs */
      .en(EN),
      .B(IN),
      .clk(CLK),
      .rst_n(RESET_B),

      /* output */
      .Wire_20(X[7]),
      .Wire_27(X[6]),
      .Wire_28(X[5]),
      .Wire_26(X[4]),
      .Wire_19(X[3]),
      .Wire_29(X[2]),
      .Wire_24(X[1]),
      .Wire_25(X[0])
    );

    initial begin

        $dumpfile("waveform/sr2.vcd");
        $dumpvars(0, sr2_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | IN=%b RESET_B=%b EN=%b CLK=%b i=%b | X=%b", $time, IN, RESET_B, EN, CLK, i[7:0], X);

        EN  = 1'b1;
        RESET_B = 1'b1;
        CLK = 1'b0;
        #10;
        RESET_B = 1'b0;
        #10;
        CLK = 1'b0;
        #10;
        CLK = 1'b1;
        #10;
        CLK = 1'b0;



        RESET_B = 1'b1;
        #10;

        // Set a single bit
        IN = 1'b1;
        #10;
        CLK = 1'b1;
        #10;
        CLK = 1'b0;
        #10;
        IN = 1'b0;

        for (i = 8'b00000001; i > 8'b0 ; i = (i << 1) & 8'b11111111)
        begin
            `assert(X, i, "Basic shifting behavior")

            EN = 1'b0;
            #10;
            CLK = 1'b1;
            #10;
            CLK = 1'b0;
            #10;
            EN = 1'b1;
            #10;

            `assert(X, i, "Clocking when EN is low has no effect")

            CLK = 1'b1;
            #10;
            CLK = 1'b0;
            #10;
        end
        `assert(X, 8'b0, "Fully passed through")

        IN = 1;
        for (i = 9'b00000001; i < 9'b100000000 ; i = (i << 1) | 9'b00000001)
        begin

            CLK = 1'b1;
            #10;
            CLK = 1'b0;
            #10;
            `assert(X, i, "Passing in constant 1's")
        end

        $finish; // End the simulation
    end

endmodule

