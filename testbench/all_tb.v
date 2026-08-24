`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

/* ref outputs/all.v */
module all_tb;

    // Inputs
    reg A;
    reg B;
    reg CLK;
    reg EN;
    reg RESET_B;

    // Outputs
    wire X;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned


    all all_1 (

      .Wire_32(A),
      .Wire_30(B),
      .Wire_3(CLK),
      .Wire_8(EN),
      .Wire_11(RESET_B),

      .Wire_33(X)
    );

    initial begin

        $dumpfile("waveform/all.vcd");
        $dumpvars(0, all_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);

        RESET_B = 1;
        EN = 1;
        CLK = 0;
        A = 0;
        B = 0;
        #10;

        RESET_B = 0;
        #10;
        RESET_B = 1'b1;
        #10;

        A = 1; B = 1;
        #10;

        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;

        A = 0; B = 0;
        #10;

        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;
        CLK = 1;
        #10;
        CLK = 0;
        #10;


        $finish; // End the simulation
    end

endmodule

