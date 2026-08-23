module xor2(
    input wire A,
    input wire B,
    output wire Y
);
    assign Y = ~(A ^ B); // Assume this is the syntax for not?
endmodule
