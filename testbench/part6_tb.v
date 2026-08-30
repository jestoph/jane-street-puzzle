`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part6.v */
module part6_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [10:0] FROM_PART8;

    // Outputs
    wire TO_OUTPUT4;
    wire TO_OUTPUT5;
    wire [1:0] MSG;

    integer i; // 32 bit
    integer j; // 32 bit

    part6 part6_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART80(FROM_PART8[0]),
      .FROM_PART81(FROM_PART8[1]),
      .FROM_PART82(FROM_PART8[2]),
      .FROM_PART83(FROM_PART8[3]),
      .FROM_PART84(FROM_PART8[4]),
      .FROM_PART85(FROM_PART8[5]),
      .FROM_PART86(FROM_PART8[6]),
      .FROM_PART87(FROM_PART8[7]),
      .FROM_PART88(FROM_PART8[8]),
      .FROM_PART89(FROM_PART8[9]),
      .FROM_PART810(FROM_PART8[10]),

      // outputs
      .TO_OUTPUT4(TO_OUTPUT4),
      .TO_OUTPUT5(TO_OUTPUT5),
      .MSG0(MSG[0]),
      .MSG1(MSG[1])

    );

    initial begin

        $dumpfile("waveform/part6.vcd");
        $dumpvars(0, part6_tb);

        clk = 0;
        S = 0;
        I = 0;
        FROM_PART8=0;
        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; S=1; I=1;


        FROM_PART8 = 11'h7ff;
        #5000; clk = ~clk;
        #5000; clk = ~clk;

        /* Look at part6, TO_OUTPUT4 is an AND of all from part8 */
        `assert(TO_OUTPUT4, 1, "Should be high");

        #5000; rst_n = 0;
        #5000; rst_n = 1;
        for( i = 0 ; i < 21; i = i + 1 )
        begin
            #5000; clk = ~clk;
            #5000; clk = ~clk;
            `assert(TO_OUTPUT5, 0, "OUTPUT5 is low for 21 clicks");
        end
        #5000; clk = ~clk;
        #5000; clk = ~clk;
        `assert(TO_OUTPUT5, 1, "OUTPUT5 is high after the 22nd click");
        #5000;
        #5000;
        #5000;
        `assert(TO_OUTPUT4, 1, "Should be high");
        `assert(TO_OUTPUT5, 1, "Should be high");


        /*
        * Exhaustive search found that all 1's works
        * Which is a pattern we already knew
        * */
        // I = 0;
        // /* Exhaustive search - there's 21 bits here */
        // for( j = 1 ; j < (1<<22); j = j + 1 )
        // begin

        //   #5000; rst_n = 0;
        //   #5000; rst_n = 1;

        //   for( i = 0 ; i < 25; i = i + 1 )
        //   begin
        //       if( ((1 << i) & j) != 0 )
        //       begin
        //         I = 1;
        //       end else begin
        //         I = 0;
        //       end
        //       #5000; clk = ~clk;
        //       #5000; clk = ~clk;
        //       `assert(TO_OUTPUT5, 0, "OUTPUT5 I HAVE FOUND THE PATTERN");
        //   end

        // end


        $finish; // End the simulation
    end

endmodule


