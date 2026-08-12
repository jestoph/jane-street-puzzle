module shift_register (
    input  wire       clk,
    input  wire        rst_n,
    input  wire        en,
    input  wire        serial_in,
    output reg  [7:0]  parallel_out
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            parallel_out <= 8'b0;
        else if (en)
            parallel_out <= {parallel_out[6:0], serial_in};
    end
endmodule

module adder8 (
    input  wire [7:0] a,
    input  wire [7:0] b,
    output wire [8:0] sum
);
    assign sum = a + b;
endmodule

module comparator496 (
    input  wire [8:0] val,
    output wire       eq
);
    assign eq = (val == 9'd496);
endmodule

module adder_demo (
    input  wire clk,
    input  wire rst_n,
    input  wire A,
    input  wire B,
    output wire S,
    input  wire en
);
    wire [7:0] a_reg, b_reg;
    wire [8:0] sum;

    shift_register sr_a (
        .clk(clk), .rst_n(rst_n), .en(en),
        .serial_in(A), .parallel_out(a_reg)
    );

    shift_register sr_b (
        .clk(clk), .rst_n(rst_n), .en(en),
        .serial_in(B), .parallel_out(b_reg)
    );

    adder8 add0 (
        .a(a_reg), .b(b_reg), .sum(sum)
    );

    comparator496 cmp0 (
        .val(sum), .eq(S)
    );
endmodule
