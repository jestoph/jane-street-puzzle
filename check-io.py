

import glob

if __name__ == '__main__':

    for file in glob.glob("component/*.v"):
        outputs = set()
        assigns = set()
        with open(file) as fp:
            for line in fp:
                if line.strip().startswith('output wire '):
                    output = line.strip().replace(",","").split()[2]
                    outputs.add(output)
                if line.strip().startswith('assign'):
                    assign = line.strip().split()[1]
                    assigns.add(assign)
        ok = (assigns == outputs)
        assert ok, f"{file=} {outputs=} {assigns=} {assigns == outputs=}"

    print("ok")
