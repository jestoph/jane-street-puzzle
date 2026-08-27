`timescale 1ns/1ps

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

/* ref outputs/part9e.v */
module part9e_tb;

    // Inputs
    reg [3:0] IN;

    // Outputs
    wire [7:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9e part9e_1 (
      //inputs
      .OB4(IN[3]),
      .OB3(IN[2]),
      .OB2(IN[1]),
      .OB1(IN[0]),
      //outputs
      .Wire_396(OUT[7]),
      .Wire_397(OUT[6]),
      .Wire_45 (OUT[5]),
      .Wire_47 (OUT[4]),
      .Wire_48 (OUT[3]),
      .Wire_49 (OUT[2]),
      .Wire_50 (OUT[1]),
      .Wire_51 (OUT[0])
    );

    initial begin

        $dumpfile("waveform/part9e.vcd");
        $dumpvars(0, part9e_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);

        IN = 0;
        for(i = 0; i <= 5'b10000; i = i + 1)
        begin
          IN = i;
          #10;
        end

        $finish; // End the simulation
    end

endmodule

