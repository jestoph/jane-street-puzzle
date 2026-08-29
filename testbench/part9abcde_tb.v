`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part9a.v */
/* ref outputs/part9b.v */
/* ref outputs/part9c.v */ // No clk
/* ref outputs/part9d.v */ // No clk
/* ref outputs/part9e.v */ // No clk
module part9abcde_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;      // I think I and S are opposite once puzzle locks?
    reg success;

    reg [3:0] MSG;

    // Outputs
    wire [7:0] OUTPUT;

    // Internal Connections

    wire [7:0] FROM_PART9A;
    wire [7:0] FROM_PART9B;
    wire [15:0] FROM_PART9C;
    wire [7:0] FROM_PART9D;
    wire [7:0] FROM_PART9E;

    integer i; // 32 bit
    integer j; // 32 bit

    part9a part9a_1 (

      // inputs
      .clk(clk),
      .success(success),

      .MSG0(MSG[0]),
      .MSG1(MSG[1]),
      .MSG2(MSG[2]),
      .MSG3(MSG[3]),

      .FROM_PART9B0(FROM_PART9B[0]),
      .FROM_PART9B1(FROM_PART9B[1]),
      .FROM_PART9B2(FROM_PART9B[2]),
      .FROM_PART9B3(FROM_PART9B[3]),
      .FROM_PART9B4(FROM_PART9B[4]),
      .FROM_PART9B5(FROM_PART9B[5]),
      .FROM_PART9B6(FROM_PART9B[6]),
      .FROM_PART9B7(FROM_PART9B[7]),

      // outputs
      .FROM_PART9A0(FROM_PART9A[0]),
      .FROM_PART9A1(FROM_PART9A[1]),
      .FROM_PART9A2(FROM_PART9A[2]),
      .FROM_PART9A3(FROM_PART9A[3]),
      .FROM_PART9A4(FROM_PART9A[4]),
      .FROM_PART9A5(FROM_PART9A[5]),
      .FROM_PART9A6(FROM_PART9A[6]),
      .FROM_PART9A7(FROM_PART9A[7]),

      .O0(OUTPUT[0]),
      .O1(OUTPUT[1]),
      .O2(OUTPUT[2]),
      .O3(OUTPUT[3]),
      .O4(OUTPUT[4]),
      .O5(OUTPUT[5]),
      .O6(OUTPUT[6]),
      .O7(OUTPUT[7])

    );

    part9b part9b_1 (

      .I(I),
      .S(S),
      .clk(clk),
      .rst_n(rst_n),

      // inputs
      .FROM_PART9A0(FROM_PART9A[0]),
      .FROM_PART9A1(FROM_PART9A[1]),
      .FROM_PART9A2(FROM_PART9A[2]),
      .FROM_PART9A3(FROM_PART9A[3]),
      .FROM_PART9A4(FROM_PART9A[4]),
      .FROM_PART9A5(FROM_PART9A[5]),
      .FROM_PART9A6(FROM_PART9A[6]),
      .FROM_PART9A7(FROM_PART9A[7]),

      .FROM_PART9C0 (FROM_PART9C[0]),
      .FROM_PART9C1 (FROM_PART9C[1]),
      .FROM_PART9C2 (FROM_PART9C[2]),
      .FROM_PART9C3 (FROM_PART9C[3]),
      .FROM_PART9C4 (FROM_PART9C[4]),
      .FROM_PART9C5 (FROM_PART9C[5]),
      .FROM_PART9C6 (FROM_PART9C[6]),
      .FROM_PART9C7 (FROM_PART9C[7]),
      .FROM_PART9C8 (FROM_PART9C[8]),
      .FROM_PART9C9 (FROM_PART9C[9]),
      .FROM_PART9C10(FROM_PART9C[10]),
      .FROM_PART9C11(FROM_PART9C[11]),
      .FROM_PART9C12(FROM_PART9C[12]),
      .FROM_PART9C13(FROM_PART9C[13]),
      .FROM_PART9C14(FROM_PART9C[14]),
      .FROM_PART9C15(FROM_PART9C[15]),

      .FROM_PART9D0 (FROM_PART9D[0]),
      .FROM_PART9D1 (FROM_PART9D[1]),
      .FROM_PART9D2 (FROM_PART9D[2]),
      .FROM_PART9D3 (FROM_PART9D[3]),
      .FROM_PART9D4 (FROM_PART9D[4]),
      .FROM_PART9D5 (FROM_PART9D[5]),
      .FROM_PART9D6 (FROM_PART9D[6]),
      .FROM_PART9D7 (FROM_PART9D[7]),

      .FROM_PART9E0 (FROM_PART9E[0]),
      .FROM_PART9E1 (FROM_PART9E[1]),
      .FROM_PART9E2 (FROM_PART9E[2]),
      .FROM_PART9E3 (FROM_PART9E[3]),
      .FROM_PART9E4 (FROM_PART9E[4]),
      .FROM_PART9E5 (FROM_PART9E[5]),
      .FROM_PART9E6 (FROM_PART9E[6]),
      .FROM_PART9E7 (FROM_PART9E[7]),


      // outputs
      .FROM_PART9B0(FROM_PART9B[0]),
      .FROM_PART9B1(FROM_PART9B[1]),
      .FROM_PART9B2(FROM_PART9B[2]),
      .FROM_PART9B3(FROM_PART9B[3]),
      .FROM_PART9B4(FROM_PART9B[4]),
      .FROM_PART9B5(FROM_PART9B[5]),
      .FROM_PART9B6(FROM_PART9B[6]),
      .FROM_PART9B7(FROM_PART9B[7])

    );

    part9c part9c_1 (

      // inputs
      .FROM_PART9A1(FROM_PART9A[1]),
      .FROM_PART9A2(FROM_PART9A[2]),
      .FROM_PART9A3(FROM_PART9A[3]),
      .FROM_PART9A4(FROM_PART9A[4]),

      // outputs
      .FROM_PART9C0 (FROM_PART9C[0]),
      .FROM_PART9C1 (FROM_PART9C[1]),
      .FROM_PART9C2 (FROM_PART9C[2]),
      .FROM_PART9C3 (FROM_PART9C[3]),
      .FROM_PART9C4 (FROM_PART9C[4]),
      .FROM_PART9C5 (FROM_PART9C[5]),
      .FROM_PART9C6 (FROM_PART9C[6]),
      .FROM_PART9C7 (FROM_PART9C[7]),
      .FROM_PART9C8 (FROM_PART9C[8]),
      .FROM_PART9C9 (FROM_PART9C[9]),
      .FROM_PART9C10(FROM_PART9C[10]),
      .FROM_PART9C11(FROM_PART9C[11]),
      .FROM_PART9C12(FROM_PART9C[12]),
      .FROM_PART9C13(FROM_PART9C[13]),
      .FROM_PART9C14(FROM_PART9C[14]),
      .FROM_PART9C15(FROM_PART9C[15])

    );

    part9d part9d_1 (

      .FROM_PART9A1(FROM_PART9A[1]),
      .FROM_PART9A2(FROM_PART9A[2]),
      .FROM_PART9A3(FROM_PART9A[3]),
      .FROM_PART9A4(FROM_PART9A[4]),

      // outputs
      .FROM_PART9D0 (FROM_PART9D[0]),
      .FROM_PART9D1 (FROM_PART9D[1]),
      .FROM_PART9D2 (FROM_PART9D[2]),
      .FROM_PART9D3 (FROM_PART9D[3]),
      .FROM_PART9D4 (FROM_PART9D[4]),
      .FROM_PART9D5 (FROM_PART9D[5]),
      .FROM_PART9D6 (FROM_PART9D[6]),
      .FROM_PART9D7 (FROM_PART9D[7])

    );

    part9e part9e_1 (

      .FROM_PART9A1(FROM_PART9A[1]),
      .FROM_PART9A2(FROM_PART9A[2]),
      .FROM_PART9A3(FROM_PART9A[3]),
      .FROM_PART9A4(FROM_PART9A[4]),

      // outputs
      .FROM_PART9E0 (FROM_PART9E[0]),
      .FROM_PART9E1 (FROM_PART9E[1]),
      .FROM_PART9E2 (FROM_PART9E[2]),
      .FROM_PART9E3 (FROM_PART9E[3]),
      .FROM_PART9E4 (FROM_PART9E[4]),
      .FROM_PART9E5 (FROM_PART9E[5]),
      .FROM_PART9E6 (FROM_PART9E[6]),
      .FROM_PART9E7 (FROM_PART9E[7])


    );

    initial begin

        $dumpfile("waveform/part9abcde.vcd");
        $dumpvars(0, part9abcde_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S=1; I=1; // try all combos
        rst_n = 0;
        success = 0;
        #5000; rst_n = 1;
        // #5000; S=0; I=0; // gives - e8e31774fae390a82ea9d494bcef8d
        // #5000; S=0; I=1; // gives - e8e31774fae390a82ea9d494bcef8d
        // #5000; S=1; I=0; // gives - e8e76ea947d04f1237fefc1f7d2834
        // #5000; S=1; I=1; // gives - e8e66dae48ce7268c3162cbe3eaf3a
        #5000; success = 1;





        for( j = 0 ; j < 5'b10000 ; j = j + 1 )
        begin
          #5000; rst_n = ~rst_n;
          #5000; rst_n = ~rst_n;
          #5000; MSG = 4'(j); // try all 16 combos


          for( i = 0 ; i < 100; i = i + 1 )
          begin
            #5000; clk = ~clk;
            #5000; clk = ~clk;

          end


        end


        $finish; // End the simulation
    end

endmodule

