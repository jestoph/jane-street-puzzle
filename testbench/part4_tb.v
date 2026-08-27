`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part4.v */
module part4_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [2:0] A;
    reg [2:0] B;
    reg [7:0] C;

    // Outputs
    wire O1;
    wire O2;

    integer i; // 32 bit
    integer j; // 32 bit

    part4 part4_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .Wire_191(C[7]),
      .Wire_370(C[6]),
      .Wire_623(C[5]),
      .Wire_624(C[4]),
      .Wire_631(C[3]),
      .Wire_647(C[2]),
      .Wire_648(C[1]),
      .Wire_649(C[0]),

      .FROM_PART52(A[2]),
      .FROM_PART51(A[1]),
      .FROM_PART50(A[0]),

      .FROM_PART7A2(B[2]),
      .FROM_PART7A1(B[1]),
      .FROM_PART7A0(B[0]),

      .TO_OUTPUT1(O1),
      .TO_OUTPUT2(O2)
    );

    initial begin

        $dumpfile("waveform/part4.vcd");
        $dumpvars(0, part4_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S = 0;
        I = 0;
        rst_n = 0;
        #5000; clk = ~clk;
        #5000; rst_n = 1;

        for( j = 0; j < 14'b10000000000000; j = j + 1)
        begin
          #5000; rst_n = 0;
          #5000; rst_n = 1;

          A = j[2:0];
          B = j[5:3];
          C = j[13:6];

          for(i = 0; i < 130 ; i = i + 1)
          begin
            #5000; clk = ~clk;
          end
          S = 1;
          for(i = 0; i < 130 ; i = i + 1)
          begin
            #5000; clk = ~clk;
          end
          I = 1;
          for(i = 0; i < 130 ; i = i + 1)
          begin
            #5000; clk = ~clk;
          end
          S = 0;
          for(i = 0; i < 130 ; i = i + 1)
          begin
            #5000; clk = ~clk;
          end
        end


        $finish; // End the simulation
    end

endmodule

