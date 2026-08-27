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

/* ref outputs/part9a.v */
module part9a_tb;

    // Inputs
    reg success;
    reg clk;
    reg [11:0] IN;

    // Outputs
    wire [7:0] OUT;
    wire [3:0] W_OUT;
    wire [3:0] W2_OUT;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    part9a part9a_1 (
      .success(success),
      .clk(clk),
      .Wire_138(IN[11]),
      .Wire_3  (IN[10]),
      .Wire_392(IN[9]),
      .Wire_393(IN[8]),
      .Wire_460(IN[7]),
      .Wire_483(IN[6]),
      .Wire_493(IN[5]),
      .Wire_494(IN[4]),
      .Wire_495(IN[3]),
      .Wire_507(IN[2]),
      .Wire_509(IN[1]),
      .Wire_510(IN[0]),
      .O7(OUT[7]),
      .O5(OUT[6]),
      .O4(OUT[5]),
      .O3(OUT[4]),
      .O6(OUT[3]),
      .O1(OUT[2]),
      .O2(OUT[1]),
      .O0(OUT[0]),
      .Wire_459(W2_OUT[3]),
      .Wire_463(W2_OUT[2]),
      .Wire_462(W2_OUT[1]),
      .Wire_461(W2_OUT[0]),
  // These feed 9c, 9d, 9e
      .OB4(W_OUT[3]),
      .OB3(W_OUT[2]),
      .OB2(W_OUT[1]),
      .OB1(W_OUT[0])

    );

    initial begin

        $dumpfile("waveform/part9a.vcd");
        $dumpvars(0, part9a_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);

        clk = 0;
        IN = 0;
        success = 0;
        for(i = 0; i <= 12'b100000000000; i = i + 1)
        begin
          #10 IN = i;
          #10;
          #10; clk = ~clk;
          #10;
          #10; clk = ~clk;
        end

        #10; clk = ~clk;
        #10; clk = ~clk;
        #10; clk = ~clk;
        #10; clk = ~clk;
        #10; clk = ~clk;

        success = 1;
        for(i = 0; i <= 12'b100000000000; i = i + 1)
        begin
          #10 IN = i;
          #10;
          #10; clk = ~clk;
          #10;
          #10; clk = ~clk;
        end

        $finish; // End the simulation
    end

endmodule

