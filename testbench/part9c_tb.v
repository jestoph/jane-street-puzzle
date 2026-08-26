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

/* ref outputs/part9c.v */
module part9c_tb;

    // Inputs
    reg [3:0] IN;

    // Outputs
    wire [15:0] OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9c part9c_1 (
      //inputs
      .Wire_100(IN[3]),
      .Wire_84 (IN[2]),
      .Wire_95 (IN[1]),
      .Wire_99 (IN[0]),
      //outputs

      .Wire_400(OUT[15]),
      .Wire_56 (OUT[14]),
      .Wire_53 (OUT[13]),
      .Wire_69 (OUT[12]),
      .Wire_466(OUT[11]),
      .Wire_59 (OUT[10]),
      .Wire_68 (OUT[9]),
      .Wire_467(OUT[8]),
      .Wire_55 (OUT[7]),
      .Wire_70 (OUT[6]),
      .Wire_60 (OUT[5]),
      .Wire_52 (OUT[4]),
      .Wire_468(OUT[3]),
      .Wire_103(OUT[2]),
      .Wire_57 (OUT[1]),
      .Wire_399(OUT[0])
    );

    initial begin

        $dumpfile("waveform/part9c.vcd");
        $dumpvars(0, part9c_tb);

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

