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

/* ref outputs/part9d.v */
module part9d_tb;

    // Inputs
    reg [3:0] IN;

    // Outputs
    wire [7:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9d part9d_1 (
      //inputs
      .Wire_100(IN[3]),
      .Wire_84 (IN[2]),
      .Wire_95 (IN[1]),
      .Wire_99 (IN[0]),
      //outputs
      .Wire_101(OUT[7]),
      .Wire_61 (OUT[6]),
      .Wire_62 (OUT[5]),
      .Wire_63 (OUT[4]),
      .Wire_64 (OUT[3]),
      .Wire_67 (OUT[2]),
      .Wire_82 (OUT[1]),
      .Wire_83 (OUT[0])
    );

    initial begin

        $dumpfile("waveform/part9d.vcd");
        $dumpvars(0, part9d_tb);

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

