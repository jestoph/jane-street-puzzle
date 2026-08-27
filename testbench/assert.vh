
`define assert(signal, value, msg) \
        if (signal !== value) begin \
            $display("ASSERTION FAILED in %m: signal (%b) != value (%b) %s", signal, value, msg); \
            $finish; \
        end

`define assertn(signal, value, msg) \
        if (signal === value) begin \
            $display("ASSERTION FAILED in %m: signal (%b) != value (%b) %s", signal, value, msg); \
            $finish; \
        end
