`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

/* ref outputs/comparitor.v */
module comparitor_tb;

    // Inputs
    reg [8:0] I;

    // Outputs
    wire X;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned


    comparitor comparitor_1 (
      // Manually worked out this ordering, is only a guess
      // as the final output must be 5 1's and 4 0's
      .Wire_105(I[8]),
      .Wire_72 (I[7]),
      .Wire_2  (I[6]),
      .Wire_71 (I[5]),
      .Wire_114(I[4]),
      .Wire_103(I[3]),
      .Wire_99 (I[2]),
      .Wire_104(I[1]),
      .Wire_112(I[0]),

      .Wire_36(X)
    );

    initial begin

        $dumpfile("waveform/comparitor.vcd");
        $dumpvars(0, comparitor_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | I=%b | X=%b", $time, I, X);

        for (i = 0; i < 9'b111111111; i = i + 1)
        begin
            I = i;
            #10;

            if( I === 9'b111110000 )
            begin
              `assert(X, 1, "Should be 1 for this value");
            end
            if( I !== 9'b111110000 )
            begin
              `assert(X, 0, "Should be 0 for all other values");
            end

        end

        $finish; // End the simulation
    end

endmodule

