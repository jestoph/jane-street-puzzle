`timescale 1ns/1ps
`include "testbench/assert.vh"

/* ref outputs/puzzle.v */
module puzzle_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg enable;

    // Outputs
    wire success;
    // wire flag;

    wire [7:0] O;

    reg flag;


    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned
    integer j; // Defaults to 32 bit int - not sure if signed or unsigned
    integer k;


    puzzle puzzle_1 (

      .I(I),
      .clk(clk),
      .enable(enable),
      .rst_n(rst_n),

      .success(success),

      .O0(O[0]),
      .O1(O[1]),
      .O2(O[2]),
      .O3(O[3]),
      .O4(O[4]),
      .O5(O[5]),
      .O6(O[6]),
      .O7(O[7])

    );

    initial begin

        $dumpfile("waveform/puzzle.vcd");
        $dumpvars(0, puzzle_tb);

        // Track changes directly in the terminal window
        /*
        $monitor("Time=%0t | I=%b clk=%b enable=%b rst_n=%b | success=%b O[0]=%b Wire_3=%b Wire_488=%b",
          $time,
          I,
          clk,
          enable,
          rst_n,
          success,
          O0,
          puzzle_1.Wire_3,
          puzzle_1.Wire_488,
        );
        */


        I = 0;
        enable = 0;
        rst_n = 0;
        clk = 0;
        flag = 0;

        /********************** EMPTY TEST CASE ****************/

        /*

        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; enable = 1;
        j = 0;
        for( i = 0 ; i < 121 ; i = i + 1)
        begin
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end
        enable = 0;

        for( i = 0 ; i < 20; i = i + 1)
        begin
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end

        */




        /********************** SPREADSHEET TEST CASE ****************/

        /* This just shows that we can get OUTPUT2 and OUTPUT3 to both be high
        *
        * see https://docs.google.com/spreadsheets/d/1TcDzKAmgSHQeR4iJsJpQ6EFZGcgxQfZcp5k93j0Eaj0/edit?gid=0#gid=0
        * */

        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; enable = 1;
        j = 0;
        for( i = 0 ; i < 121 ; i = i + 1)
        begin

          #5000;
          case (i)



            0: I = 1;
            1: I = 0;
            2: I = 0;
            3: I = 0;
            4: I = 1;
            5: I = 0;
            6: I = 0;
            7: I = 0;
            8: I = 0;
            9: I = 0;
            10: I = 0;
            11: I = 0;
            12: I = 0;
            13: I = 0;
            14: I = 0;
            15: I = 0;
            16: I = 0;
            17: I = 1;
            18: I = 0;
            19: I = 1;
            20: I = 0;
            21: I = 0;
            22: I = 1;
            23: I = 0;
            24: I = 0;
            25: I = 1;
            26: I = 0;
            27: I = 0;
            28: I = 0;
            29: I = 0;
            30: I = 0;
            31: I = 0;
            32: I = 0;
            33: I = 0;
            34: I = 0;
            35: I = 0;
            36: I = 0;
            37: I = 0;
            38: I = 1;
            39: I = 0;
            40: I = 1;
            41: I = 0;
            42: I = 0;
            43: I = 0;
            44: I = 1;
            45: I = 0;
            46: I = 0;
            47: I = 0;
            48: I = 0;
            49: I = 0;
            50: I = 0;
            51: I = 0;
            52: I = 0;
            53: I = 1;
            54: I = 0;
            55: I = 0;
            56: I = 0;
            57: I = 1;
            58: I = 0;
            59: I = 1;
            60: I = 0;
            61: I = 0;
            62: I = 0;
            63: I = 0;
            64: I = 0;
            65: I = 0;
            66: I = 1;
            67: I = 0;
            68: I = 0;
            69: I = 0;
            70: I = 0;
            71: I = 0;
            72: I = 1;
            73: I = 0;
            74: I = 0;
            75: I = 0;
            76: I = 0;
            77: I = 0;
            78: I = 0;
            79: I = 1;
            80: I = 0;
            81: I = 1;
            82: I = 0;
            83: I = 0;
            84: I = 0;
            85: I = 0;
            86: I = 0;
            87: I = 0;
            88: I = 1;
            89: I = 0;
            90: I = 0;
            91: I = 0;
            92: I = 0;
            93: I = 0;
            94: I = 1;
            95: I = 0;
            96: I = 0;
            97: I = 0;
            98: I = 0;
            99: I = 0;
            100: I = 0;
            101: I = 1;
            102: I = 0;
            103: I = 0;
            104: I = 0;
            105: I = 0;
            106: I = 0;
            107: I = 1;
            108: I = 0;
            109: I = 0;
            110: I = 1;
            111: I = 0;
            112: I = 0;
            113: I = 0;
            114: I = 0;
            115: I = 1;
            116: I = 0;
            117: I = 0;
            118: I = 0;
            119: I = 0;
            120: I = 0;



            default: begin `assert(1,0, "Should never get here"); end
          endcase

          #5000; clk = ~clk;
          #5000;
          #5000; clk = ~clk;

          `assert(puzzle_1.TO_OUTPUT2, 1, "???");


        end

        enable = 0;

        for( i = 0 ; i < 20; i = i + 1)
        begin
          #5000; clk = ~clk;
          #5000; clk = ~clk;
        end


        $finish; // End the simulation
    end

endmodule

