`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part7.v */
/* ref outputs/part5.v */
/* ref outputs/part4.v */
module part754_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg flag;

    reg [4:0] FROM_PART2;

    // Internal
    /* verilator lint_off UNDRIVEN */
    wire [2:0] FROM_PART7A; // Want to be 7
    wire [6:0] FROM_PART7B; // Want to be 0xfe (actually I don't think we care about the upper bit?)
    wire FROM_PART7C0;      // Not sure what we want here? I think 1?
    wire [2:0] FROM_PART5;

    // Outputs
    wire TO_OUTPUT1;
    wire TO_OUTPUT2;
    wire TO_OUTPUT3;

    integer i; // 32 bit
    integer j; // 32 bit


    part7 part7_1 (

      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART20(FROM_PART2[0]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART23(FROM_PART2[3]),

      // outputs
      .FROM_PART7A0(FROM_PART7A[0]),
      .FROM_PART7A1(FROM_PART7A[1]),
      .FROM_PART7A2(FROM_PART7A[2]),

      .FROM_PART7B1(FROM_PART7B[0]),
      .FROM_PART7B2(FROM_PART7B[1]),
      .FROM_PART7B3(FROM_PART7B[2]),
      .FROM_PART7B4(FROM_PART7B[3]),
      .FROM_PART7B5(FROM_PART7B[4]),
      .FROM_PART7B6(FROM_PART7B[5]),
      .FROM_PART7B7(FROM_PART7B[6]),

      .FROM_PART7C0(FROM_PART7C0)

    );

    part4 part4_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART7B7(FROM_PART7B[6]),
      .FROM_PART7B6(FROM_PART7B[5]),
      .FROM_PART7B5(FROM_PART7B[4]),
      .FROM_PART7B4(FROM_PART7B[3]),
      .FROM_PART7B3(FROM_PART7B[2]),
      .FROM_PART7B2(FROM_PART7B[1]),
      .FROM_PART7B1(FROM_PART7B[0]),

      .FROM_PART7C0(FROM_PART7C0),

      .FROM_PART52(FROM_PART5[2]),
      .FROM_PART51(FROM_PART5[1]),
      .FROM_PART50(FROM_PART5[0]),

      .FROM_PART7A2(FROM_PART7A[2]),
      .FROM_PART7A1(FROM_PART7A[1]),
      .FROM_PART7A0(FROM_PART7A[0]),

      // outputs
      .TO_OUTPUT1(TO_OUTPUT1),
      .TO_OUTPUT2(TO_OUTPUT2)
    );

    part5 part5_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),

      .FROM_PART20(FROM_PART2[0]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART24(FROM_PART2[4]),

      .FROM_PART50(FROM_PART5[0]),
      .FROM_PART51(FROM_PART5[1]),
      .FROM_PART52(FROM_PART5[2]),

      .TO_OUTPUT3(TO_OUTPUT3)
    );





    initial begin

        $dumpfile("waveform/part754.vcd");
        $dumpvars(0, part754_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);


        /****************************
        * MAP BITS TO OUTPUT
        *****************************/

        /* When A is zero, the output should be B */
        clk = 0;
        S = 0;
        I = 0;
        rst_n = 0;
        FROM_PART2 = 0;
        #5000; rst_n = 1;
        #5000; S=1; I=1;

        for( j = 0 ; j < 6'b100000 ; j = j + 1 )
        begin

          // #5000; rst_n = ~rst_n;
          // #5000; rst_n = ~rst_n;

          FROM_PART2 = 5'(j);

          for( i = 0 ; i < 2 ; i = i + 1 )
          begin
            #5000; clk = ~clk;
            #5000; clk = ~clk;

          end

          if(FROM_PART7B == 7'h7f)
          begin
            flag = 1;
          end
          if(FROM_PART7B != 7'h7f)
          begin
            flag = 0;
          end

        end


        $finish; // End the simulation
    end

endmodule
// `timescale 1ns/1ps
// `include "testbench/assert.vh"
// 
// /* ref outputs/part4.v */
// module part4_tb;
// 
//     // Inputs
//     reg I;
//     reg rst_n;
//     reg clk;
//     reg S;
//     reg [2:0] FROM_PART5;
//     reg [2:0] FROM_PART7A;
//     reg [6:0] FROM_PART7B;
//     reg FROM_PART7C;
// 
//     // Outputs
//     wire TO_OUTPUT1;
//     wire TO_OUTPUT2;
// 
//     integer i; // 32 bit
//     integer j; // 32 bit
// 
//     part4 part4_1 (
//       // Inputs
//       .I(I),
//       .rst_n(rst_n),
//       .clk(clk),
//       .S(S),
// 
//       .FROM_PART7B7(FROM_PART7B[6]),
//       .FROM_PART7B6(FROM_PART7B[5]),
//       .FROM_PART7B5(FROM_PART7B[4]),
//       .FROM_PART7B4(FROM_PART7B[3]),
//       .FROM_PART7B3(FROM_PART7B[2]),
//       .FROM_PART7B2(FROM_PART7B[1]),
//       .FROM_PART7B1(FROM_PART7B[0]),
// 
//       .FROM_PART7C0(FROM_PART7C),
// 
//       .FROM_PART52(FROM_PART5[2]),
//       .FROM_PART51(FROM_PART5[1]),
//       .FROM_PART50(FROM_PART5[0]),
// 
//       .FROM_PART7A2(FROM_PART7A[2]),
//       .FROM_PART7A1(FROM_PART7A[1]),
//       .FROM_PART7A0(FROM_PART7A[0]),
// 
//       // outputs
//       .TO_OUTPUT1(TO_OUTPUT1),
//       .TO_OUTPUT2(TO_OUTPUT2)
//     );
// 
//     initial begin
// 
//         $dumpfile("waveform/part4.vcd");
//         $dumpvars(0, part4_tb);
// 
//         // Track changes directly in the terminal window
//         // $monitor("Time=%0t | A=%b B=%b | X[8]=%b X[7:0]=%b", $time, A, B, X[8], X[7:0]);
// 
// 
//         /****************************
//         * MAP BITS TO OUTPUT
//         *****************************/
// 
//         /* When A is zero, the output should be B */
//         clk = 0;
//         S = 1'bx; //1;      // S seems to have no impact?
//         I = 1'bx;
//         rst_n = 0;
// 
//         #5000; rst_n = 1;
// 
//         FROM_PART5  = 3'bx;
//         FROM_PART7A = 7;
//         FROM_PART7B = 7'h7f;
//         FROM_PART7C = 1;
// 
//         #5000;
// 
//         `assert(TO_OUTPUT1, 1, "Should be high with this pattern")
//         `assert(TO_OUTPUT2, 1, "Should be high with this pattern")
// 
// 
// 
//         $finish; // End the simulation
//     end
// 
// endmodule
// 
// `timescale 1ns/1ps
// `include "testbench/assert.vh"
// 
// /* ref outputs/part5.v */
// module part5_tb;
// 
//     // Inputs
//     reg I;
//     reg rst_n;
//     reg clk;
//     reg S;
//     reg [4:0] FROM_PART2;
//     reg Hello;
// 
//     // Outputs
//     wire OUTPUT;
//     wire [2:0] FROM_PART5;
// 
//     integer i; // 32 bit
//     integer j; // 32 bit
// 
//     part5 part5_1 (
//       // Inputs
//       .I(I),
//       .rst_n(rst_n),
//       .clk(clk),
//       .S(S),
// 
//       .FROM_PART20(FROM_PART2[0]),
//       .FROM_PART21(FROM_PART2[1]),
//       .FROM_PART22(FROM_PART2[2]),
//       .FROM_PART23(FROM_PART2[3]),
//       .FROM_PART24(FROM_PART2[4]),
// 
//       .FROM_PART50(FROM_PART5[0]),
//       .FROM_PART51(FROM_PART5[1]),
//       .FROM_PART52(FROM_PART5[2]),
// 
//       .TO_OUTPUT3(OUTPUT)
//     );
// 
//     initial begin
// 
//         $dumpfile("waveform/part5.vcd");
//         $dumpvars(0, part5_tb);
// 
//         // Track changes directly in the terminal window
//         // $monitor("Time=%0t | FROM_PART2=%b | OUTPUT=%b", $time, FROM_PART2, OUTPUT);
// 
// 
//         /****************************
//         * MAP BITS TO OUTPUT
//         *****************************/
// 
//         /* When A is zero, the output should be B */
//         clk = 0;
//         S = 0;
//         I = 0;
//         rst_n = 0;
//         Hello = 0;
//         FROM_PART2 = 0;
//         #5000; rst_n = 1;
//         #5000; S=1; I=1;
// 
//         for( j = 0; j < 6'b100000; j = j + 1)
//         begin
//           #5000; rst_n = 0;
//           #5000; rst_n = 1;
// 
//           #5000; FROM_PART2 = 5'(j);
// 
//           #5000; clk = ~clk;
//           #5000; clk = ~clk;
// 
//           `assertn(OUTPUT, FROM_PART2[4], "Output is opposite of bit 5");
// 
//         end
// 
// 
//         $finish; // End the simulation
//     end
// 
// endmodule
// 
