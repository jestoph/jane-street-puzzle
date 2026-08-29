`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/part6.v */
/* ref outputs/part8.v */
/* ref outputs/blob.v */
module partblob86_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [3:0] FROM_PART2;
    reg [3:0] FROM_PART3;

    // Outputs
    wire TO_OUTPUT4;
    wire TO_OUTPUT5;
    wire [1:0] MSG;

    // internal
    reg [3:0] FROM_BLOB;
    wire [10:0] FROM_PART8;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned
    integer j; // Defaults to 32 bit int - not sure if signed or unsigned

    blob blob_1 (

      .FROM_PART23(FROM_PART2[3]),
      .FROM_PART22(FROM_PART2[2]),
      .FROM_PART21(FROM_PART2[1]),
      .FROM_PART20(FROM_PART2[0]),

      .FROM_PART33(FROM_PART3[3]),
      .FROM_PART32(FROM_PART3[2]),
      .FROM_PART31(FROM_PART3[1]),
      .FROM_PART30(FROM_PART3[0]),

      .FROM_BLOB3(FROM_BLOB[3]),
      .FROM_BLOB2(FROM_BLOB[2]),
      .FROM_BLOB1(FROM_BLOB[1]),
      .FROM_BLOB0(FROM_BLOB[0])

    );

    part8 part8_1 (
      // Inputs
      .I(I),
      .rst_n(rst_n),
      .clk(clk),
      .S(S),


      .FROM_BLOB0(FROM_BLOB[0]),
      .FROM_BLOB1(FROM_BLOB[1]),
      .FROM_BLOB2(FROM_BLOB[2]),
      .FROM_BLOB3(FROM_BLOB[3]),

      // outputs
      // outputs - want this to be 11'h7ff;
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
      .FROM_PART810(FROM_PART8[10])
    );

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

        $dumpfile("waveform/partblob86.vcd");
        $dumpvars(0, partblob86_tb);

        // Track changes directly in the terminal window
        // $monitor("Time=%0t | A=%b B=%b CLK=%b EN=%b RESET_B=%b | X=%b", $time, A, B, CLK, EN, RESET_B, X);
        clk = 0;
        S = 1;
        I = 1;
        rst_n = 0;
        #5000; rst_n = 1;
        FROM_PART2 = 0;
        FROM_PART3 = 0;

        for(j = 0; j <= 11'b10000000000; j = j + 1)
        begin
          #10;
          FROM_PART2 = 4'(j);
          FROM_PART3 = 4'(j);
          for( i = 0 ; i < 22; i = i + 1 )
          begin
              #5000; clk = ~clk;
              #5000; clk = ~clk;
          end
        end

        $finish; // End the simulation
    end

endmodule

// `timescale 1ns/1ps
// `include "testbench/assert.vh"
// 
// /* ref outputs/part8.v */
// module part8_tb;
// 
//     // Inputs
//     reg I;
//     reg rst_n;
//     reg clk;
//     reg S;
//     reg [3:0] FROM_BLOB;
// 
//     // Outputs
//     wire [10:0] FROM_PART8;
// 
//     integer i; // 32 bit
//     integer j; // 32 bit
// 
//     part8 part8_1 (
//       // Inputs
//       .I(I),
//       .rst_n(rst_n),
//       .clk(clk),
//       .S(S),
// 
// 
//       .FROM_BLOB0(FROM_BLOB[0]),
//       .FROM_BLOB1(FROM_BLOB[1]),
//       .FROM_BLOB2(FROM_BLOB[2]),
//       .FROM_BLOB3(FROM_BLOB[3]),
// 
//       // outputs
//       .FROM_PART80(FROM_PART8[0]),
//       .FROM_PART81(FROM_PART8[1]),
//       .FROM_PART82(FROM_PART8[2]),
//       .FROM_PART83(FROM_PART8[3]),
//       .FROM_PART84(FROM_PART8[4]),
//       .FROM_PART85(FROM_PART8[5]),
//       .FROM_PART86(FROM_PART8[6]),
//       .FROM_PART87(FROM_PART8[7]),
//       .FROM_PART88(FROM_PART8[8]),
//       .FROM_PART89(FROM_PART8[9]),
//       .FROM_PART810(FROM_PART8[10])
//     );
// 
//     initial begin
// 
//         $dumpfile("waveform/part8.vcd");
//         $dumpvars(0, part8_tb);
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
//         S = 1; // Can also be 0
//         I = 1; // Can also be 0
//         rst_n = 0;
//         FROM_BLOFROM_PART3 = 0;
//         #5000; rst_n = 1;
//         #5000; S=1; I=1;
// 
//         for( j = 0 ; j < 5'b10000 ; j = j + 1 )
//         begin
// 
//           // #5000; rst_n = ~rst_n;
//           // #5000; rst_n = ~rst_n;
// 
//           FROM_BLOFROM_PART3 = 4'(j);
// 
//           for( i = 0 ; i < 2; i = i + 1 )
//           begin
//             #5000; clk = ~clk;
//             #5000; clk = ~clk;
// 
//           end
// 
// 
//         end
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
// /* ref outputs/part6.v */
// module part6_tb;
// 
//     // Inputs
//     reg I;
//     reg rst_n;
//     reg clk;
//     reg S;
//     reg [10:0] FROM_PART8;
// 
//     // Outputs
//     wire TO_OUTPUT4;
//     wire TO_OUTPUT5;
//     wire [1:0] MSG;
// 
//     integer i; // 32 bit
//     integer j; // 32 bit
// 
//     part6 part6_1 (
//       // Inputs
//       .I(I),
//       .rst_n(rst_n),
//       .clk(clk),
//       .S(S),
// 
//       .FROM_PART80(FROM_PART8[0]),
//       .FROM_PART81(FROM_PART8[1]),
//       .FROM_PART82(FROM_PART8[2]),
//       .FROM_PART83(FROM_PART8[3]),
//       .FROM_PART84(FROM_PART8[4]),
//       .FROM_PART85(FROM_PART8[5]),
//       .FROM_PART86(FROM_PART8[6]),
//       .FROM_PART87(FROM_PART8[7]),
//       .FROM_PART88(FROM_PART8[8]),
//       .FROM_PART89(FROM_PART8[9]),
//       .FROM_PART810(FROM_PART8[10]),
// 
//       // outputs
//       .TO_OUTPUT4(TO_OUTPUT4),
//       .TO_OUTPUT5(TO_OUTPUT5),
//       .MSG0(MSG[0]),
//       .MSG1(MSG[1])
// 
//     );
// 
//     initial begin
// 
//         $dumpfile("waveform/part6.vcd");
//         $dumpvars(0, part6_tb);
// 
//         clk = 0;
//         S = 0;
//         I = 0;
//         #5000; rst_n = 0;
//         #5000; rst_n = 1;
//         #5000; S=1; I=1;
// 
// 
//         FROM_PART8 = 11'h7ff;
//         for( i = 0 ; i < 22; i = i + 1 )
//         begin
//             #5000; clk = ~clk;
//             #5000; clk = ~clk;
//         end
//         #5000;
//         #5000;
//         #5000;
//         `assert(TO_OUTPUT4, 1, "Should be high");
//         `assert(TO_OUTPUT5, 1, "Should be high");
// 
// 
//         $finish; // End the simulation
//     end
// 
// endmodule
// 
