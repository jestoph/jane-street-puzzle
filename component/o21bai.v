module o21bai(
    input wire A1,
    input wire A2,
    input wire B1_N,
    output wire Y
);
    // TODO: https://sky130-unofficial.readthedocs.io/en/latest/contents/libraries/sky130_fd_sc_hd/cells/o21bai/README.html
    assign Y = ~((A1 | A2) & (~B1_N));
endmodule
