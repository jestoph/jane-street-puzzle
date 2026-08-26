

import glob

if __name__ == '__main__':

    for file in glob.glob("component/*.v"):
        outputs = set()
        inputs = set()
        assigns = set()
        assign_line = ""
        with open(file) as fp:
            for line in fp:
                if line.strip().startswith('output wire '):
                    output = line.strip().replace(",","").split()[2]
                    outputs.add(output)
                if line.strip().startswith('input wire '):
                    _input = line.strip().replace(",","").split()[2]
                    inputs.add(_input)
                if line.strip().startswith('assign'):
                    assign_line = line
                    assign = line.strip().split()[1]
                    assigns.add(assign)
        ok = (assigns == outputs)
        assert ok, f"{file=} {outputs=} {assigns=} {assigns == outputs=}"

        for _input in inputs:
            if 'diode' not in file and 'df' not in file:
                assert _input in assign_line, f"{_input=} not in '{assign_line}' -> {file}"

    print("ok")
