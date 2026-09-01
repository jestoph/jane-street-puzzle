`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal (%b) != value (%b) %s", signal, value, msg); \
            $finish; \
        end

/* ref outputs/puzzle.v */
module puzzle_tb;

    // Inputs
    reg I; reg rst_n; reg clk; reg enable;

    // Outputs
    wire success;

    wire [7:0] O;

    // Iterator
    integer i; // Defaults to 32 bit int - not sure if signed or unsigned


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



        I = 0;
        enable = 0;
        rst_n = 0;
        clk = 0;



        /* I want FROM_PART80 to go high at clock 120 */

        #5000; rst_n = 0;
        #5000; rst_n = 1;
        #5000; enable = 1;
        for( i = 0 ; i < 121 ; i = i + 1)
        begin


          case(i)

            0: I = 0;
            1: I = 0;
            2: I = 0;
            3: I = 0;
            4: I = 0;
            5: I = 0;
            6: I = 0;
            7: I = 1;
            8: I = 0;
            9: I = 1;
            10: I = 0;
            11: I = 1;
            12: I = 0;
            13: I = 0;
            14: I = 0;
            15: I = 0;
            16: I = 1;
            17: I = 0;
            18: I = 0;
            19: I = 0;
            20: I = 0;
            21: I = 0;
            22: I = 0;
            23: I = 0;
            24: I = 0;
            25: I = 0;
            26: I = 0;
            27: I = 0;
            28: I = 0;
            29: I = 1;
            30: I = 0;
            31: I = 1;
            32: I = 0;
            33: I = 1;
            34: I = 0;
            35: I = 1;
            36: I = 0;
            37: I = 0;
            38: I = 0;
            39: I = 0;
            40: I = 0;
            41: I = 0;
            42: I = 0;
            43: I = 0;
            44: I = 0;
            45: I = 0;
            46: I = 0;
            47: I = 0;
            48: I = 1;
            49: I = 0;
            50: I = 1;
            51: I = 0;
            52: I = 0;
            53: I = 0;
            54: I = 0;
            55: I = 0;
            56: I = 0;
            57: I = 1;
            58: I = 0;
            59: I = 0;
            60: I = 0;
            61: I = 0;
            62: I = 0;
            63: I = 1;
            64: I = 0;
            65: I = 0;
            66: I = 0;
            67: I = 0;
            68: I = 0;
            69: I = 0;
            70: I = 1;
            71: I = 0;
            72: I = 0;
            73: I = 0;
            74: I = 0;
            75: I = 0;
            76: I = 1;
            77: I = 0;
            78: I = 1;
            79: I = 0;
            80: I = 0;
            81: I = 0;
            82: I = 0;
            83: I = 1;
            84: I = 0;
            85: I = 0;
            86: I = 0;
            87: I = 0;
            88: I = 0;
            89: I = 0;
            90: I = 0;
            91: I = 1;
            92: I = 0;
            93: I = 0;
            94: I = 0;
            95: I = 0;
            96: I = 0;
            97: I = 0;
            98: I = 1;
            99: I = 0;
            100: I = 0;
            101: I = 0;
            102: I = 0;
            103: I = 0;
            104: I = 1;
            105: I = 0;
            106: I = 0;
            107: I = 1;
            108: I = 0;
            109: I = 0;
            110: I = 0;
            111: I = 1;
            112: I = 0;
            113: I = 1;
            114: I = 0;
            115: I = 0;
            116: I = 0;
            117: I = 0;
            118: I = 0;
            119: I = 0;
            120: I = 0;
            121: I = 0;

            default: begin `assert(1,0, "Should never get here"); end
          endcase

          #5000; clk = ~clk;
          #5000;
          #5000; clk = ~clk;



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

