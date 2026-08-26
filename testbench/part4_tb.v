`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal (%b) != value (%b) %s", signal, value, msg); \
            $finish; \
        end

/* ref outputs/part4.v */
module part4_tb;

    // Inputs
    reg I;
    reg rst_n;
    reg clk;
    reg S;
    reg [13:0] IN;

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
      .Wire_9(S),
      .Wire_184(IN[13]),
      .Wire_189(IN[12]),
      .Wire_192(IN[11]),
      .Wire_290(IN[10]),
      .Wire_371(IN[9]),
      .Wire_446(IN[8]),
      .Wire_448(IN[7]),
      .Wire_449(IN[6]),
      .Wire_624(IN[5]),
      .Wire_625(IN[4]),
      .Wire_632(IN[3]),
      .Wire_648(IN[2]),
      .Wire_649(IN[1]),
      .Wire_650(IN[0]),
      // outputs
      .Wire_222(O1),
      .Wire_491(O2)
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
        IN = 0;
        rst_n = 0;
        #5000; clk = ~clk;
        #5000; rst_n = 1;

        for( j = 0; j < 14'b10000000000000; j = j + 1)
        begin
          #5000; rst_n = 0;
          #5000; rst_n = 1;
          IN = j;
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

