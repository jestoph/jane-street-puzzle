
## What's in a GDS file?

Rather than googling, lets have a look. There's familiar words like 'clk' (clock), 'rst' (reset) and 'VGND' and 'VPWR' (ground and power).

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

## What's in the circuit simulation?

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

Here we need to do a huge yak shave and of course build our own circuit simulator. We'll need at a very minimum the following elements
```
Standard circuit elements - wires, and, clk, mux, nand, nor, inv, (is 'inv' a 'not'?), xor, xnow, adder
diode - Implies we'll need high impedance as a value. I hope we won't need analogue signals like pull downs
buf - Maybe this is like a register? So we'll need edge triggers some how
```

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

## Looking at gds file

|          cell_name                 | cnt  | Ideas
|----------------------------------------------------
|`sky130_fd_sc_hd__and2_2`           |      | and
|`sky130_fd_sc_hd__and4bb_2`         |      | and - maybe 4-port?
|`sky130_fd_sc_hd__and3_2`           |      | another and?
|`sky130_fd_sc_hd__xor2_2`           |      | xor
|`sky130_fd_sc_hd__xnor2_2`          |      | xnor
|`sky130_fd_sc_hd__or2_2`            |      | or
|`sky130_fd_sc_hd__nand2_2`          |      | nand
|`sky130_fd_sc_hd__mux2_1`           |      | 2-bit mux?
|`sky130_fd_sc_hd__nor2_2`           |      | nor
|`sky130_fd_sc_hd__clkbuf_16`        |      | Looks to just help distribute the clk signal
|`VIA_M2M3_PR`                       |      | Power rail?
|`sky130_fd_sc_hd__dfrtp_2`          | 16   | Some sort of flip flop (see sky-130 unofficial below)
|`sky130_fd_sc_hd__tapvpwrvgnd_1`    |      | Looks like pins to power and ground - can probably ignore
|`sky130_fd_sc_hd__decap_3`          |      | Maybe debouncing capacitors - they're at the edge so I think I can ignore them
|`sky130_fd_sc_hd__a31o_2`           | 5    | Maybe io?
|`sky130_fd_sc_hd__a21o_2`           | 1    | Maybe io?
|`sky130_fd_sc_hd__a21boi_2`         | 1    | Maybe io?
|`sky130_fd_sc_hd__o21bai_2`         | 1    | Maybe io?
|`sky130_fd_sc_hd__a21bo_2`          | 2    | Maybe io?
|`adder_demo`                        | 1    | Whole module
|`VIA_via5_6_2000_2000_1_1_1600_1600`| lots | some sort of via
|`VIA_via4_5_2000_480_1_5_400_400`   | lots | some sort of via
|`VIA_M1M2_PR`                       | lots | some sort of via
|`VIA_via3_4_2000_480_1_5_400_400`   | lots | some sort of via
|`VIA_M3M4_PR`                       | lots | some sort of via
|`VIA_via2_3_2000_480_1_6_320_320`   | lots | some sort of via
|`VIA_L1M1_PR_MR`                    | lots | some sort of via

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

It's on the top right, so I would guess x>8000 and y>70000 should roughly do it.

Ok not at all, it was way harder than I though. Things seem to be normalised to the range (0,100) or something,
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

    library.write_gds("logo.gds")
```



if __name__ == '__main__':
    logo()



### What are those sky things anyway?

Google is my friend - https://sky130-unofficial.readthedocs.io/en/latest/
