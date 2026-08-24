`timescale 1ns/1ps

`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal != value %s", msg); \
            $finish; \
        end

/* ref outputs/adder.v */
module adder_tb;

    // Inputs
    reg [7:0] A;
    reg [7:0] B;

    // Outputs
    wire [8:0] X;

    adder adder_1 (
      /*input A */
      .Wire_1(A[0]),
      .Wire_12(A[1]),
      .Wire_25(A[2]),
      .Wire_9(A[3]),
      .Wire_30(A[4]),
      .Wire_13(A[5]),
      .Wire_32(A[6]),
      .Wire_14(A[7]),

      /*input B */
      .Wire_21(B[0]),
      .Wire_28(B[1]),
      .Wire_26(B[2]),
      .Wire_20(B[3]),
      .Wire_24(B[4]),
      .Wire_29(B[5]),
      .Wire_27(B[6]),
      .Wire_10(B[7]),

      /*outputs*/
      .Wire_114(X[0]),
      .Wire_103(X[1]),
      .Wire_72(X[2]),
      .Wire_2(X[3]),
      .Wire_99(X[4]),
      .Wire_112(X[5]),
      .Wire_71(X[6]),
      .Wire_104(X[7]),
      .Wire_105(X[8])
    );

    initial begin

        $dumpfile("waveform/adder.vcd");
        $dumpvars(0, adder_tb);

        // Track changes directly in the terminal window
        $monitor("Time=%0t | A=%b B=%b | X=%b", $time, A, B, X);

        A = 8'b11111111 ; #10;

        $finish; // End the simulation
    end

endmodule

