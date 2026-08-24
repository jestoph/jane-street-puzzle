module a21bo(
    input wire A1,
    input wire A2,
    input wire B1_N,
    output wire X
);
    // TODO: The doc says 'or' but the picture shows 'and'?
    // https://sky130-unofficial.readthedocs.io/en/latest/contents/libraries/sky130_fd_sc_hd/cells/a21bo/README.html
    assign X = ~(~(A1 & A2) & B1_N);
endmodule
