import sys
from common import IO_PORTS
import os

if __name__ == '__main__':
    for name in IO_PORTS:
        ins = IO_PORTS[name][0]
        outs = IO_PORTS[name][1]
        pretty_name = name.replace("_1","").replace("_2","")
        io = []
        for _in in sorted(ins):
            io.append(f"  input wire {_in}")
        for _out in sorted(outs):
            io.append(f"  output wire {_out}")
        io = ",\n".join(io)
        content = []
        content.append(f"module {pretty_name}(")
        content.append(io)
        content.append(f");")
        content.append("    /* TODO: provide implementation */")
        content.append(f"endmodule")

        path = f"component/{pretty_name}.v"
        if os.path.exists(path):
            print(f"SKIPPING {pretty_name}")
        else:
            print(f"Writing {pretty_name}")
            with open(path, "w") as fp:
                print("\n".join(content), file=fp)
