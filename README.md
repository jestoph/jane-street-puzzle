
## Challenge Accepted

Hey this looks fun. There's some file called 'gds' and some verilog or something. I have a EE degree that's rotting away unused in my
brain somewhere, could be good to learn something.

### What's in the files?

Rather than googling, lets have a look at these files. There's familiar words like 'clk' (clock), 'rst' (reset) and 'VGND' and
'VPWR' (ground and power).

There's a bunch of `sky130...` whatever things. If we strip that we get a more managable set of things. We'll start with the example that's
a bit smaller and group them together

```term
% strings warmup/04_final.gds | sed 's/sky130_fd_sc_hd__//g' | sort | uniq -c
  25 @3333334
   3 a21bo_2
   3 a21boi_2
   3 a21o_2
   7 a31o_2
   1 adder_demo
   9 and2_2
   3 and3_2
   4 and4bb_2
   3 B1_N
   5 clkbuf_16
  60 decap_3
  18 dfrtp_2
  18 mux2_1
   6 nand2_2
  10 nor2_2
   3 o21bai_2
   7 or2_2
   2 RESET_B
   1 rst_n
  95 tapvpwrvgnd_1
  21 VGND
 269 VIA_L1M1_PR_MR
 314 VIA_M1M2_PR
  46 VIA_M2M3_PR
   6 VIA_M3M4_PR
  76 VIA_via2_3_2000_480_1_6_320_320
  76 VIA_via3_4_2000_480_1_5_400_400
  76 VIA_via4_5_2000_480_1_5_400_400
  14 VIA_via5_6_2000_2000_1_1_1600_1600
  21 VPWR
   5 xnor2_2
   7 xor2_2
```
Taking them one at a time:
* `@3333334` No idea - but the main project has a bunch. Maybe some divisor or clock?
* `and2_2`, `and3_2`, `and4bb_2`
* `VIA_L1M1_PR_MR`, `VIA_via2_3_2000_480_1_6_320_320` etc. Some sort of vias, maybe the name mangling defines which layers they connect between?
* The rest seem like normal circuit elements, like `or`, `mux` etc. We'll need all of these in our circuit simulator
* No idea what `B1_N`, `decap_3`, `dfrtp_2`, `tapvpwrvgnd_1` are
* The following all have a pattern that I can't decipher `a21bo_2`, `a21boi_2` etc. Maybe they're nodes?

There's a library 'gdstk' in python that seems to be able to read them. It gives 27 elements rather than 33 above. Good start

```Bash
% python3 -c 'print(len(__import__("gdstk").read_gds("warmup/04_final.gds").cells))'
27
```

### What's in the circuit simulation?

I can see in the example_inputs.vcd that there's some signal being sent in or something when the character '%' is present. Maybe I can grep it?

```Term
$ grep '\%$' example_inputs.vcd
bx %
b0 %
b1010100 %
b1010010 %
b1011001 %
b100000 %
b1000001 %
b1000111 %
b1000001 %
b1001001 %
b1001110 %
b0 %
b1010100 %
b1010010 %
b1011001 %
b100000 %
b1000001 %
b1000111 %
b1000001 %
b1001001 %
b1001110 %
b0 %
```

It looks like characters (7 bit ascii maybe?). Let's see

```C
#include <stdio.h>

char chrs[] = {
// 0bx ,         // I think this is 'unknown' or 'high impedance' or something?
0b0 ,
0b1010100 ,
0b1010010 ,
0b1011001 ,
0b100000 ,
0b1000001 ,
0b1000111 ,
0b1000001 ,
0b1001001 ,
0b1001110 ,
0b0 ,
0b1010100 ,
0b1010010 ,
0b1011001 ,
0b100000 ,
0b1000001 ,
0b1000111 ,
0b1000001 ,
0b1001001 ,
0b1001110 ,
0b0 ,
};

int main(){

  for(int i = 0 ; i < sizeof(chrs)/sizeof(chrs[0]); i++){
    printf("%c ", chrs[i]);
  }
  printf("\n")

}
```

Running that gives

```Term
$ ./a.out
T R Y   A G A I N  T R Y   A G A I N
```

Ok we're on to something

## On building a circuit simulator

Here we need to do a huge yak shave and of course build our own circuit simulator. For reasons. We'll need at a
very minimum the following elements from the list of strings above

* Standard circuit elements - wires, and, clk, mux, nand, nor, inv, (is 'inv' a 'not'?), xor, xnow, adder
* diode - Implies we'll need high impedance as a value. I hope we won't need analogue signals like pull downs
* buf - Maybe this is like a register? So we'll need edge triggers some how

### Several days later

Ok so I built a circuit sim using sqlite3 as a driver. Quite neat really. But it's quite hard to design circuits in Python!
If only there was a language for describing hardware.

### Several days later

Ok so I built a parser for my new language and now I can design circuits. But I need to test them! If only there was some
way of scriptings inputs and validating outputs.

### Several days later

Ok so I built a harness for my circuit simulator. But it's really hard to visualise what it's doing!

### Several days later

Ok so I built a waveform and circuit viewer in Raylib. Where were we again?

## Looking at the actual gds file

I was able to roughly annotate the circuit visually with the tinytapeout tool [img](annotated01.jpg) but I'm a bit
unsure about which of rst_n or and are which - I can see that clk, en and rst_n would all feed to both shift
registers, and was able to guess clk because it feeds into the clkbuf elements (I guess as its a signal that is
distributed it needs some buffering/amplification). I just guessed A and B would be top and bottom, respectively.
This turned out to be correct.

I'll look at the actual file and see what I can do

### The actual file

I spent some time with binary tools but didn't make too much sense of it - I don't really understand things like -

* Why are layers not named? The tool seems to know the names but I can't see them in the file
* What cells are what? Are they wires? There's so many
* Some labels have things like 'clk' in there - I guess I should look at them?
* There are labels in the file that are really useful - but why aren't they displayed in the viewer?

It's hard to parse from a binary but I found a translator to text instead

```bash
$ pip install python-gdsii
$ gds2txt warmup/04_final.gds > output.txt
```

Looking at that file, it was easy to see that there's a text section under 'adder' the has the signals I care about.
A bit of vim magic and I can sort them numerically to distinguish rst_n and en

```
TEXT LAYER: 70 TEXTTYPE: 5 XY: 300, 30260 STRING: "en" ENDEL
TEXT LAYER: 70 TEXTTYPE: 5 XY: 300, 35700 STRING: "B" ENDEL
TEXT LAYER: 70 TEXTTYPE: 5 XY: 300, 41140 STRING: "A" ENDEL
TEXT LAYER: 70 TEXTTYPE: 5 XY: 300, 57460 STRING: "rst_n" ENDEL
TEXT LAYER: 70 TEXTTYPE: 5 XY: 300, 73780 STRING: "clk" ENDEL
TEXT LAYER: 70 TEXTTYPE: 5 XY: 99700, 16660 STRING: "S" ENDEL
TEXT LAYER: 71 TEXTTYPE: 5 XY: 26440, 50320 STRING: "VPWR" ENDEL
TEXT LAYER: 71 TEXTTYPE: 5 XY: 30140, 50320 STRING: "VGND" ENDEL
```

Actually it turns out that the yaml format is even more convenient -

```
% gds2yaml warmup/04_final.gds > output.yaml
% jless output.yaml
```

I had 'clk' as the top-left signal, so I guess (0,0) is at the bottom left rather than the top right like in
image processing. So now I have all the input and output signals. And the differenced between the points look
about right - there's roughly twice the distance between A and B as between A and rst_n.

A good start.

Helpfully this also gives us a rough way of finding elements as I guess we have min(x,y)/max(x,y) of roughly
* min_x=0
* min_y=0
* max_x=17000 roughly?
* max_y=100000 eyeballing it

So theoretically I should be able to extract just the jane street logo, right?

### On extracting the logo

It's on the top right, so I would guess x>8000 and y>70000 should roughly do it. Right?

No not at all, it was way harder than I thought. Things seem to be normalised to the range (0,100) or something,
and there's the concept of repetitions that makes it hard to exactly tell where things are.

I'm still confused about
* Paths can have multiple layers somehow
* But polygons don't? I don't understand that

Anyway layers are back-to-front. The logo is on layer 69. I've removed almost all paths and polygons, but
somehow there are still elements and cells in the library. I'm not sure how to completely remove cells in
code, maybe the library I'm using doesn't expose that.

```python
import gdstk
def logo():
    library = gdstk.read_gds("warmup/04_final.gds")

    for cell in library.cells:
        for poly in cell.polygons:
            (min_x, min_y), _ = poly.bounding_box()
            if min_x < 50 or min_y < 50:
                cell.remove(poly)

    for cell in library.cells:
        for path in cell.paths:
            cell.remove(path)

    library.write_gds("outputs/logo.gds")
if __name__ == '__main__':
    logo()
```

It turns out later that this worked by accident as I didn't understand yet that each cell uses its own coordinates
so this was just filtering out 'small' elements, and the top adder element happens to be large. The filtering on
the adder looks to be correct though.

### What are layer and data types?

Looking at the layer types, it seems that all layers from 64 to 72 have type '20', so that must be metal, which
I'll need for analysing how wires connect.

```
% make stats | grep datatype=20
   layer=64 datatype=20
   layer=65 datatype=20
   layer=66 datatype=20
   layer=67 datatype=20
   layer=68 datatype=20
   layer=69 datatype=20
   layer=70 datatype=20
   layer=71 datatype=20
   layer=72 datatype=20    # <- All good up to here
   layer=94 datatype=20    # <- Wait, what?
   layer=95 datatype=20
```
But what's with the wierd gaps? It seems there's no layer 73 for example,
but the viewer shows no spaces. Does the format just implicitly say that missing layers are filled in with a
previous line?

Anyway, what data types do we have anyway?

```
% make stats | grep -o 'datatype=\d*' | sort -n | uniq -c
   1 datatype=0   # <- Probably the base layer I guess, maybe plastic or epoxy?
   2 datatype=4
   7 datatype=16
  11 datatype=20  # <- metal I guess
   9 datatype=44
```

I also now realise that the axes of the whole design are in (0,0), (100,100) rather than the units in the text
file from gds2txt. What's that about? Is that just a gdstk library thing? I'd prefer to work in consistent
units

### Ok time to look at the individual elements

There's 27 elements, lets get a good look at all of them.

```python
import gdstk

def cells(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:
        name = cell.name
        cell.write_svg(f"outputs/{name}.svg")
        lib = gdstk.Library(name)
        lib.add(cell)
        lib.write_gds(f"outputs/{name}.gds")


if __name__ == '__main__':
    cells("warmup/04_final.gds")
```

### What can I see in the SVGs?

The design is much clearer to understand with all the labels! And the wires are all the same size now which is nice. I can
really get a sense for it in this format

Now lets look at the 'sky130' components.

file            | Best-Guess  | In            | Out | notes
----------------------------------------------------------------------------------------------------------------------------------------
`a21bo_2`       |             | A1,A2         | X   | A1, A2 on right, B1_N on middle, X on left
`a21boi_2`      |             | A1,A2,B1_N    | Y   | A1, A2 on right, B1_N on left, Y in middle
`a21o_2`        |             | A1,A2,B1      | X   | A1's, A2 on right, B1 in middle, X top right
`a31o_2`        |             | A1,A2,A3,B1   | X   | A1, A2, A3 in middle, B1 on right, X's on left
`o21bai_2`      |             | A1,A2,B1_N    | Y   | B1_N & A1 and A2 on middle (reflected vertically), Y on upper area
`and2_2`        | AND         | A,B           | X   | A on left, B middle, X's right
`and3_2`        | 3-port AND  | A,B,C         | X   | A left, B & C middlish, X on right
`and4bb_2`      | 4-port AND  | A_N,B_N,C,D   | X   | A_N left, X's mid-left, C's and a D mid-right, B_N on right
`clkbuf_16`     | clk buffer  | A             | X   | A on left X's on right - Looks like a basic buffer, I think I can emulate this as a 'Nop' element in my sim
`mux2_1`        | 2-bit mux   |               | S   | Complicated. A0, A1's, S's (S=Signal?) towards middle, X's on left
`nand2_2`       | NAND        | A,B           | Y   | A & B on middle, Y's on right
`nor2_2`        | NOR         | A,B           | Y   | A & B on middle strip, Y on upper right
`or2_2`         | OR          | A,B           | X   | B & A in middle strip, X on upper right
`xnor2_2`       | XNOR        |               | Y   | B on top half, A on middle strip, Y on right
`xor2_2`        | XOR         |               | X   | A top left, B on middle strip, X on right
`dfrtp_2`       | flip flop?  | D,CLK,RESET_B | Q   | CLK, D, Q, RESET_B. Looks like a flip flop of some sort.
`decap_3`       | decaps      |               |     | Definitely decoupling/filtering capacitor, only connected to rails
`tapvpwrvgnd_1` | power feed? |               |     | Seems to allow connecting to pwr/gnd throughout. In the main circuit it always cuts through the busses

* The pattern seems to be `<type><input port count>_<something>`, not sure what the 'something' is yet.
* Power seems to be always at the top and gnd at the bottom in the default rotation of the elements.
* Not much to say about the via nodes, but it's interesting that vias are so complicated. And some are multi-port?
* There is visual overlap between VPB & VPWR, and VNB & VGND on all of them. Are they the same things?
* I can't remember how flip flops work. Wikipedia says this is probably a D flip-flop as has D, Q and clk, and
  they form the basis of shift registers, so I guess that's what they are.
* I need to learn about these ones - `a21bo_2`, `a21boi_2`, `a21o_2`, `a31o_2`, `o21bai_2`. There's some structure
  to the names (`i` seems to mean that B is negated, the first number is the number of A inputs, maybe the
  second number is the number of outputs and just always happens to be 1)
* It seems the output of the mux is our output signal 'S'. Maybe these labels are partially derived from our
  verilog names? But I'm not sure what that means for signals like A3.

If I ignore vias for now (TODO: assuming they have 'metal' as the datatype), then there's only 16 circuit elements
that I need to understand

### Time to actually read

I've gotten as far as I can with guessing. Time to actually read some proper documentation.
Looks like this is their home, despite the 'unofficial' in the name - `https://sky130-unofficial.readthedocs.io/en/latest/`


Ok. The docs had the answers to many of my questions. Why do I always do things the hard way?
* The sky130 is 130 nanometer tech
* The layer sizes, datatypes and names are all defined in the document!
  https://sky130-unofficial.readthedocs.io/en/latest/rules/layers.html#gds-layers-information
* It _does_ look like 20 is often or always metal
* All the cells and renderings and ports are listed here https://sky130-unofficial.readthedocs.io/en/latest/contents/libraries/sky130_fd_sc_hd/README.html
* I was _roughly_ correct in my table above, but missed some details

The big conclusion here is that I think I can start at the geometries in the 'local interconnect' layer (66:44) as I believe
that is where the 'pins' or 'pads' or whatever they're called on the devices are, then I only have to map out these geometries to I/O ports.

Luckily, the library I'm using has a 'filter' method, so lets try that

```python
for cell in library.cells:
    cell.filter([(67, 20)], remove=False, polygons=True, paths=True, labels=False)
    cell.write_svg(f"outputs/{cell.name}.li.svg")
```
Looking at the output, that works almost perfectly, so now I can theoretically map specific geometry to the I/O of the circuit elements.
My only slight concern is that the labels might be referenced by a corner rather than by their centerpoint, so I might need to do some
math on that


That worked ... way better than I expected! I guess labels are already referenced on their centerpoint! It even picked up some geometry
that isn't visually connected so a visual inspection would never have revealed their connections. And looking at the total design's
IO ports, it's so much less visually noisey [here](outputs/adder_demo.li.io.svg)


## I think I can make a graph now?

This isn't going to be easy. When I flatten out the top element (adder_demo), it has 1k paths and almost 17k polygons.
I thought that filtering on datatype=20 would clean things up but after filtering it barely made a dint.

I can simplify the filtering when searching for 'touching' pairs by doing the following.
1. Filter out simple elements (see list below)
2. Create an Index by layer
3. For a given element, only check adjacent layers
4. Filter initially on bounding box overlap - 4 float comparisons
5. Finaly check for true overlap

If I need to I could also chunk up the total area as a step 2a.

I'm not sure the total number of elements now, but in the order of thousands, this might be tough for graph traversal

### Elements I'm pretty sure I don't care about

* Layers below 67 (signal pins/pads)
* Layers above 70 (It looks like 71/met4 is a power bus not a signal), and also via3 that only connects to met4
* That gives the following layer/datatypes - li1, mcon, met1, via, met2, via2, met3
* VIA_via elements? Not 100% sure, but there's 225 of them. There's also many paths that _only_ connect to them
* 'Filter Cells' - a nice tinytapeout feature toggles these
  * The decap elements (58 of them)
  * The tapvpwrvgnd (93 elements)
* There's many isolated cells/paths on met3 once the filter cells are removed
* The logo

If I do that, I 'should' be able to create a dot graph of the network.

### Finding all connected components

1. Filter out all elements as above
2. Start with 'li1' layer with valid IO ports
3. Step by layer, keeping all elements that touch an existing element
  - sequence is li1, mcon, met1, via (should be called via1 I think?), met2, via2, met3

It will be an O(M x N) calculation where M is the number of elements on layer i and N is the number of elements on layer i+1.

Ok so that has some obvious directional artifacts but shows that I'm at least able to filter connected components. I need a
better flood fill or bfs-style algorithm and I should be able to get the whole graph

