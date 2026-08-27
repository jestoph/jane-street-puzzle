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

/* ref outputs/blob.v */
module blob_tb;

    // Inputs
    reg [7:0] IN;

    // Outputs
    wire [3:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    blob blob_1 (

      .Wire_315(IN[7]),
      .Wire_110(IN[6]),
      .Wire_129(IN[5]),
      .Wire_79 (IN[4]),
      .Wire_309(IN[3]),
      .Wire_80 (IN[2]),
      .Wire_28 (IN[1]),
      .Wire_71 (IN[0]),

      .BLOB3(OUT[3]),
      .BLOB2(OUT[2]),
      .BLOB1(OUT[1]),
      .BLOB0(OUT[0])

    );

    initial begin

        $dumpfile("waveform/blob.vcd");
        $dumpvars(0, blob_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);
        IN = 0;

        for(i = 0; i <= 9'b100000000; i = i + 1)
        begin
          #10;
          IN = i[7:0];
          `assertn(OUT[3], 1'bx, "Signal should not be x");
          `assertn(OUT[2], 1'bx, "Signal should not be x");
          `assertn(OUT[1], 1'bx, "Signal should not be x");
          `assertn(OUT[0], 1'bx, "Signal should not be x");
        end

        $finish; // End the simulation
    end

endmodule

