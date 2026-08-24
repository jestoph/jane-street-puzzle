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

    integer i;


    sr1 sr1_1 (
      /* inputs */
      .Wire_8(EN),
      .Wire_35(IN),
      .Wire_3(CLK),
      .Wire_11(RESET_B),

      /* output - Manually specified */
      .Wire_9 (X[7]),
      .Wire_24(X[6]),
      .Wire_1 (X[5]),
      .Wire_32(X[4]),
      .Wire_12(X[3]),
      .Wire_14(X[2]),
      .Wire_10(X[1]),
      .Wire_13(X[0])
    );

    initial begin

        $dumpfile("waveform/sr1.vcd");
        $dumpvars(0, sr1_tb);

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
            CLK = 1'b1;
            #10;
            CLK = 1'b0;
            #10;
        end
        `assert(X, 8'b0, "Fully passed through")

        $finish; // End the simulation
    end

endmodule

