`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/output_section.v */
module output_section_tb;

    // Inputs
    reg rst_n;
    reg clk;
    reg [5:0] IN;

    // Outputs
    wire A;
    wire B;
    wire success;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned

    output_section output_section_1 (
      .rst_n(rst_n),
      .clk(clk),
      .TO_OUTPUT5(IN[5]),
      .TO_OUTPUT4(IN[4]),
      .TO_OUTPUT3(IN[3]),
      .TO_OUTPUT2(IN[2]),
      .TO_OUTPUT1(IN[1]),
      .TO_OUTPUT0(IN[0]),

      .Wire_138(A),
      .Wire_3(B),
      .success(success)

    );

    initial begin

        $dumpfile("waveform/output_section.vcd");
        $dumpvars(0, output_section_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);
        IN = 0;
        rst_n = 0;
        clk = 0;
        #5000; clk = 1;
        rst_n = 1;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        #5000; clk = 0;

        // IN = 6'b000100;
        // #5000; clk = ~clk;
        // #5000; clk = ~clk;
        // `assert(success, 0, "???");
        // `assert(A, 0, "???");
        // `assert(B, 1, "???");

        // rst_n = 0;
        // #5000;
        // rst_n = 1;
        // #5000;
        // IN = 6'b111111;
        // #5000; clk = ~clk;
        // #5000; clk = ~clk;
        // `assert(success, 1, "success should be high");
        // `assert(A, 0, "???");
        // `assert(B, 1, "???");

        // rst_n = 0;
        // #5000;
        // rst_n = 1;
        // #5000;


        for(i = 7'b0000000; i <= 7'b1000000; i = i + 1)
        begin
          rst_n = 0;
          #5000;
          rst_n = 1;
          #5000;
          IN = i[7:0];
          #5000; clk = ~clk;
          #5000; clk = ~clk;
          #5000;
          `assertn(A, 1'bx, "Signal should not be x");
          `assertn(B, 1'bx, "Signal should not be x");
          `assertn(success, 1'bx, "Signal should not be x");
        end

        // `assert(success, 0, "Success won't go high if B is high first?");
        // `assert(A, 0, "Success won't go high if B is high");
        // `assert(B, 1, "Success won't go high if B is high");

        // rst_n = 0;
        // #5000;
        // rst_n = 1;
        // #5000; clk = 0;
        // for(i = 7'b0111111; i <= 7'b1000000; i = i - 1)
        // begin
        //   IN = i[7:0];
        //   // if( in[2:1] == 4'b11)
        //   // begin
        //   //   // 0c 0d 0e 0f
        //   //   `assert(B, 1, "B is high when mask")
        //   // end

        //   // if( in[2:1] === 4'b10)
        //   // begin
        //   //   // 0c 0d 0e 0f
        //   //   `assert(B, 1, "B is high when mask")
        //   // end
        //   #5000; clk = ~clk;
        //   #5000; clk = ~clk;
        //   `assertn(A, 1'bx, "Signal should not be x");
        //   `assertn(B, 1'bx, "Signal should not be x");
        //   `assertn(success, 1'bx, "Signal should not be x");
        // end

        // `assert(success, 1, "Success won't go high if B is high");
        // `assert(B, 1, "Success won't go high if B is high");

        $finish; // End the simulation
    end

endmodule

