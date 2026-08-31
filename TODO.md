
## Warmup Circuit

### Viewing the circuit
[x] Find some way of laying out the circuit. Maybe use 'schemdraw' which does it in python. - This is a dead end I think?
[x] Try with
  [x] Comparitor
  [-] Shift Register 1
  [-] Shift Register 2
  [-] Adder
  [-] Total Circuit

### Simulating the circuit
[x] Kill my circuit simulator
[x] Add all warmup cells to iverilog and testbenches
[x] Work out how to name io wires - Hard-coded for now
[x] Work out how to Write output as vcd - quite easy to do I think - https://zipcpu.com/blog/2017/07/31/vcd.html
[x] Add real assertions to component behaviours
[x] Have real tests of all components
[x] Build test-benches of
  [x] Comparitor
  [x] Adder
  [x] Shift Register 1
  [x] Shift Register 2
[x] Run real test sims of
  [x] Comparitor
  [x] Shift Register 1
  [x] Shift Register 2
  [x] Adder
[x] What is the deal with a21bo? https://sky130-unofficial.readthedocs.io/en/latest/contents/libraries/sky130_fd_sc_hd/cells/a21bo/README.html
[x] Fix issue with different clocks for sr1 and sr2. They should be the same. Maybe due to clckbuf issue?
[x] Test bench of Total Circuit
[x] Sim of Total Circuit


### GDS Tooling - Abandon this!
[x] Find a local GDS viewer - could I use Raylib + voxels? Probably not a good idea but ....
  [x] Start gds viewer in raylib - steal an example
  [x] Fix orthographic view in examples - relies on rcamera and possibly rmath, can probably copy-paste
  [x] Draw up my understanding of raylib camera perspectives (first/third person, orthographic) in xcalidraw
  [x] Get standard camera movements working -
    [x] Pan
    [x] Zoom
    [x] Drag/rotate
  [x] Try to place some elements for a small cell
    [x] Bounding Boxes
    [x] How to turn a polygon into blocks? - I think this is going to be harder than I thought - might need to make mesh models
[x] I think this is a lost cause - I don't understand raylib enough to get this working

### Starting ideas
[x] Start trying to extract the network
[x] Extract all unique cells to individual gds and svg using a makefile
[x] Work out coordinate system of the file
[x] Work out how to filter on global coords rather than local - maybe flatten all top cells, and do it by bounding box?
[x] Turn this into a proper repo on my github
[x] Create a realtime-updating svg viewer? - No, not needed. Chrome does a good-enough job

### Understanding the network
[x] Try to understand individual cells
  [x] Look at circuit elements made by cells.py
  [x] Work out how to show labels (maybe convert to text?) and add them to cells.py - Was done already in svg function
  [x] Look at obscured labels under PWR and GND labels
  [x] Read the manual - https://sky130-unofficial.readthedocs.io/en/latest/
  [x] Can I map labels on io ports to geometry?
[x] Draw up my understanding of gds in xcalidraw - not necessary, it's all spelled out in the docs
[x] Map out the graph
  [x] Try to find a single example of a circuit element connected to a wire and write it to a gds
  [x] Build a gds of all connected, useful/interesting components
      - Got one working but with 'directional' artifacts. The naive algorithm isn't the best
  [x] Use a proper flood fill or graph traversal algorithm - layer connection worked fine
  [x] Fix bounding box issue
  [x] Work out how to take multiple distinct wires and convert into a single wire
  [x] Try to build a dot file (might need to give each pad a unique name like `AND:123:A -> MUX:7:Q` or something like that) - instead going with schemdraw
  [x] Add Validations
     [x] Warn on unconnected pins
     [x] No output pins connected to inputs
     [x] Check that all port names exist etc
  [x] Understand via scripts the following elements:
     [x] Comparitor
      [x] Auto-detect outputs and inputs
     [x] Shift Register 1
      [x] Auto-detect outputs and inputs
     [x] Shift Register 2
      [x] Fix bug <- I have two wires connected to only one component
      [x] Auto-detect outputs and inputs
     [x] Adder <- not feeling confident this will work
      [x] Fix via4/met4 information
      [x] Auto-detect outputs and inputs
      [x] Get all components in to simulator - they are stateless
      [x] Write tests for all of them

### Basic validation
[x] Check all cells are showing ports correctly - they all look OK
[x] Check stats
[x] Check can read circuit
[x] Check can simplify - some errors I'll need to resolve
[x] Simplify the following:
  [x] All clkbufs just wires
  [x] All bufs are just wires
[x] Add implementations for components
  [x] 2 x flip-flops ('df') components
  [x] 12 x 'a' components
  [x] 14 x 'o' components
[x] What are the diodes doing? Why does my filter still include with end bits? Why are they in the circuit?
  [x] Should I include them? I can see they have some things attached.... Treating the pads as wires
[x] Get input and output wire aliases working
  [x] Detect aliases
  [x] Use in outputs
[x] Fix errors in simplify step
[ ] Work out the behavioural differences between 'dfrtp', 'dfstp', 'dfxtp' flip-flops

### Simplify Network by working backwards from output

[x] Output errors on `O[7:0]` are likely due to issues with `Wire_3` or `Wire_488` as they're the common wires across all the outputs- nope was bad components
[x] Consider breaking the larger sections out
 [x] outputs/part7.json <- could be 3 sections
 [x] outputs/part9.json <- could be 5 sections
[x] Fix detection of inputs and outputs - two heuristics should help. Still not perfect, but will do for now
[x] Confirm that regions are correct for the simple regions
 [x] outputs/part1.json
 [x] outputs/part2.json
 [x] outputs/part3.jsonv
 [x] outputs/part4.json <- Probably a 12 or 13 bit shift register! Has 13 x drftp and 12 x mux like in warmup puzzle
 [x] outputs/part5.json
 [x] outputs/part6.json
 [x] outputs/part7a.json
 [x] outputs/part7c.json
 [x] outputs/part9a.json - Seems to generate some signal, i think it sends out 'reads' and pushes the response to the output port?
      It also has the behaviour of clocking through all the values, then stopping (all outputs go high). There are 14 values, with
      0 before anything happens and F after it's all done
 [x] outputs/part9c.json
 [x] outputs/part9d.json
 [x] outputs/part9e.json
 [x] outputs/output_section.json
 [x] outputs/blob.json - is probably fine as has no memory
[x] Confirm that regions are correct for the less simple regions
 [x] outputs/part7b.json
 [x] outputs/part8.json
 [x] outputs/part9b.json

### Understand top-down information of circuit
[x] Rename appropriate areas to be busses instead
[x] Draw on excalidraw
[x] BUG! Wire_536 is driven in two circuits! But somehow not getting picked up? Was a slight overlap in areas.
    Added a validation check to prevent it again
[x] Draw out inter-section maps - it's confusing at the moment but maybe there's structure?

### Run Simulations
[x] Output section - Got pattern `5'b11111` as the 'success' pattern, other patterns with output A and B though.
    Seems if you latch the B signal you'll never get a success though, and it latches on half the patterns
[x] Write test benches for easy ones:
 [x] outputs/blob.v - was easy as doesn't contain any flipflops so is fully io determined
 [x] outputs/part1.v -> Latches in when the two inputs and 'enable' is high. When enable is high, the output and
     'S' seem to always be inverted?
 [x] outputs/part2.v -> Some sort of lfsr or something? It cycles through 12 values
 [x] outputs/part3.v -> Another lfsr? This time 11 values.
 [x] outputs/part4.v -> Shift register with an 'enable' via muxes on Wire_9/S
 [x] Output generation circuit:
     [x] outputs/part9a.v -> Got this working but then overwrote the file and now it's not behaving that same!
     [x] outputs/part9c.v -> Easy
     [x] outputs/part9d.v -> Easy
     [x] outputs/part9e.v <- Should have been easy but there's an undriven wire! `a31oi:A1 <-> a311o:A1`
 [x] outputs/output_section.v

### Working on undriven wire
[x] Add ability to set the pin to a label
[x] Run sim with random pin set to
 [x] A1 -> 'Works' as in validation succeeds
 [x] A2 -> Results in wire driven by two outputs
 [x] A3 -> Results in wire driven by two outputs
 [x] B1 -> Results in wire driven by two outputs
 [x] Y -> Results in wire driven by two outputs

### Quality-of-life
[x] Move wires to be `Wire_<n>`
[x] Move ports etc to be `<type>_<n>.<pin>`. The colon is annoying
[x] I've added warning for dangling wires. Can I promote them to error? Yep just checking the stderr

## Questions/Concerns
[ ] What are 'boundaries' in the gds2text output?
[ ] Why does the text file have more types?
[ ] What is the pattern in the example input? Does it give a hint?
[ ] I guessed behaviour of 'dfst' and 'dfxtp'. Were these guesses correct?
[ ] What are `INTERNAL_3` and `INTERNAL_7`? Do they have a location?
[ ] Should I add a validation step to find any other mcon elements connected to random pins?
[ ] Was it the correct move to connect the undriven wire? Would the true password appear if it wasn't connected?
[x] What happens to `FROM_PART7B[0]` - it's internal to PART7

## NEXT as of Thu 27 Aug 2026
[x] Write testbenches for the hard ones - roughly in ascending order of difficulty:
 [x] outputs/part7c.v -> Actually not too complicated. It seems to go high on the second A&B input, then low on the third?
 [x] outputs/part5.v
 [x] outputs/part6.v
 [x] outputs/part7a.v - Actually got it to produce the '7' output that part4 needs - takes 6 clocks
 [x] outputs/part7b.v - got it to produce the 0x7f that part4 needs
 [x] outputs/part8.v - Managed to get 0x7ff which is what part6 needs
 [x] outputs/part9b.v -> Did it but it wasn't particularly insightful


## How to make the 6 bits go high?
[x] One bit from Part 1 - two inputs and 'enable' is high, and/or after 121 clock cycles after a reset
[x] Two bits from Part 4 - Got it, a certain pattern from part 7a,b,c and the rest literally doesn't matter.
[x] One bit from Part 5 - Got it - when S&I and bit 5 of FROM_PART2 is low.
[x] Two bits from part 6 - Got it - input=0x7ff, S&I, and 22 clocks
[x] Make minimal examples

## Next as of Fri 28 Aug 2026 - Understand each logical division, try to get output message working
[x] Test new logical divisions -
 [x] testbench/part123_tb.v - Could act like a signal generator, with a single output bit?
      It's also like a timer! That's why you have 121 clocks to get your password in
      Now down to only 2^121 bits, less than the numbers of atoms in the universe! Also it disables
      the rest by setting the S to low after 121 clocks, which I guess lets part9 do its thing.
 [x] Part 9a,b,c,d,e 'should' be easy enough to get an output from. It would at least prove that things aren't
     broken - because when I simulate the whole circuit I get no output.
 [x] Part 9 fully extracted - Got it identical, so I guess things are internally consistent
 [x] Part 7a,b,c is relatively small -> Got all three outputs to be the right value
 [x] Part 7 fully extracted -> Got matching output (But what's the deal with the goes-nowhere output?)
 [x] Part 5,7,4 is self contained and has 3 output bits
 [x] Part Blob,8,6 has two output bits -> Could not get this to output the correct bits - it will need time

## Next Sat 29 Aug 2026
[x] Draw out the circuit for the easy candidates:
 [x] outputs/output_section.v
 [x] outputs/part4.v -> Was OK! Just a shift register and some other junk
[x] Trace back the bits
 [x] Bit 0 -> From part1 on a timer
 [x] Bit 1
 [x] Bit 2 -> Seems to not line pulses on I
 [x] Bit 3 -> Seems to not rely on input at all, just on value of part2
 [x] Bit 4
 [x] Bit 5

### TRY TO GET TO_OUTPUT3 TO STAY ALIVE

- TO_OUTPUT0 goes high after 121 clocks
- TO_OUTPUT3 wants two (or more?) clocks as a 'keep-alive' within every 11 clock. I tested all variations and they all worked
- TO_OUTPUT5 seems to be similar, it comes in later if OUTPUT3 is high
- TO_OUTPUT2 goes LOW after three rising edges of I signal TO_OUTPUT3
- I've only seen OUTPUT1 and OUTPUT5 high when I is high the whole time

### Looking at part 4
There is a shift register that feeds some bits into a logical section

| bit | dfrtp | mux | wire
------------------------------
| 0   | 43    | 8   | `Wire_639`
| 1   | 53    | 3   | `Wire_641`
| 2   | 45    | 2   | `Wire_642`
| 3   | 52    | 4   | `Wire_643`
| 4   | 44    | 12  | `Wire_443`
| 5   | 49    | 5   | `Wire_651`
| 6   | 42    | 6   | `Wire_652`
| 7   | 54    | 7   | `Wire_653`
| 8   | 50    | 13  | `Wire_654`
| 9   | 51    | 11  | `Wire_444`
| 10  | 48    | 9   | `Wire_442`
| 11  | 46    | 10  | `Wire_640`

Looking at the final structure, TO_OUTPUT1 will go high if all of PART7's outputs are high, but TO_OUTPUT2 is quite tricky. It
depends on the values of the signal generator and the input, plus some delayed values from the input via the shift register

Part5 seems to only have three patterns -
 - 3'b011
 - 3'b101
 - 3'b111
 This is correct as part5 basically proxies the output from part2, and the top bit is a `conb.HI` element


[x] Encode two known behaviours of part4 in to the test bench
 [x] When all PART7 outputs are high, TO_OUTPUT1 is high
 [x] The shift register
 [x] The logic for latching TO_OUTPUT2
[x] Draw out circuit for part5 as OUTPUT3 relies on it
 [x] Proxy is simple
 [ ] The rest is deceptively complicated
[x] Build a part12345 testbench that aimt to set output2 and output3 to show how to solve it
 [x] Encode understanding of IO from PART24 and I into the testbench
 [x] Actually I just encoded this in the puzzle itself
[ ] Build a part1237 testbench that works out how to set all outputs of 7 to 1


Is part7c just a popcount? It seems that if popcnt(FROM_PART2) > 1 then it is high? Not quite - in the sim
it doesn't quite do that



```
  // ref component/nor4.v
  nor4 nor4_1 (
    .A(FROM_PART21),
    .B(FROM_PART22),
    .C(FROM_PART23),
    .D(FROM_PART20),
    .Y(FROM_PART7B0) // output to part 7c
  );
```

## Working on Part 7 Outputs
- Part 7c is surprisingly tricky. I haven't been able to work it out

## Working on TO_OUTPUT4
- Turns out part6 proxies all of part8 as a big AND for TO_OUTPUT4
- But 8 is fed from BLOB. BLOB is relatively simple though
- Turns out part8 is 11 repetitions of a similar structure. If there was some way of cracking each element I'd have a solution


## HOW TO SOLVE THE DOUBLE FLIP FLOP ISSUE??????

I get that theres some recurrance relationship that I can use but I can't quite work it out
```
O1_0, O1_1 = 0,0                              # Because we have a reset
O1_n+1, O2_n+1 = fn(O1_n, O2_n, BLOB_n, I_n)  # Defined for each section
O1_121, O2_121 = <desired final value>        # Defined for each section

```

There are libraries sympy and z3, I've used z3 before.

Maybe we can solve them backwards?
