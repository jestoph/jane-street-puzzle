

import glob

if __name__ == '__main__':

    for file in glob.glob("outputs/part*.v"):
        with open(file) as fp:
            for lineno, line in enumerate(fp):
                if line.strip().startswith('output wire '):
                    output = line.strip().replace(",","").split()[2]
                    assert 'Wire_' not in output, f"Wire {output} in {file}:{lineno} is unnamed"
                if line.strip().startswith('input wire '):
                    _input = line.strip().replace(",","").split()[2]
                    assert 'Wire_' not in _input, f"Wire {_input} in {file}:{lineno} is unnamed"
    print("ok")
