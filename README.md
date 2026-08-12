
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

Can I render the labels so I can see where and what is labelled?


## I think I can make a graph now?

This isn't going to be easy. When I flatten out the top element (adder_demo), it has 1k paths and almost 17k polygons.
I thought that filtering on datatype=20 would clean things up but after filtering it barely made a dint.

I can simplify the filtering when searching for 'touching' pairs by doing the following.
1. Create an Index by layer
2. For a given element, only check adjacent layers
3. Filter initially on bounding box overlap - 4 float comparisons
4. Finaly check for true overlap

If I need to I could also chunk up the total area as a step 2a.

If I do that, I 'should' be able to create a dot graph of the network.

Luckily there are only 233 circuit elements (with prefix 'sky'), and I think I can exclude the 'decap' elements as
they seem to be signal decoupling capacitors on the edge of the circuit. That brings it down to 175 circuit elements.

So the real challenge is following wires I think


### What are those sky things anyway?
Google is my friend - https://sky130-unofficial.readthedocs.io/en/latest/
