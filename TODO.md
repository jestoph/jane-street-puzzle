## Questions
[ ] What are boundaries in the gds2text output?
[ ] Why does the text file have more types?

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

## Real Circuit

[ ] What is the pattern in the example input? Does it give a hint?
[ ] I guessed behaviour of 'dfst' and 'dfxtp'. Were these guesses correct?
[ ] What are `INTERNAL_3` and `INTERNAL_7`?

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
[ ] Fix detection of inputs and outputs - two heuristics should help
[x] Confirm that regions are correct for the simple regions
 [x] outputs/part1.json
 [x] outputs/part2.json
 [x] outputs/part3.jsonv
 [x] outputs/part4.json <- Probably a 12 or 13 bit shift register! Has 13 x drftp and 12 x mux like in warmup puzzle
 [x] outputs/part5.json
 [x] outputs/part6.json
 [x] outputs/part7a.json
 [x] outputs/part7c.json
 [x] outputs/part9a.json
 [x] outputs/part9c.json
 [x] outputs/part9d.json
 [x] outputs/part9e.json
 [x] outputs/output_section.json
 [x] outputs/blob.json - is probably fine as has no memory
[ ] Confirm that regions are correct for the less simple regions
 [ ] outputs/part7b.json
 [ ] outputs/part8.json
 [ ] outputs/part9b.json

### Run Simulations
[x] Output section - Got pattern `5'b11111` as the 'success' pattern, other patterns with output A and B though.
    Seems if you latch the B signal you'll never get a success though, and it latches on half the patterns
[ ] Write test benches for:
 [x] outputs/blob.v - was easy as doesn't contain any flipflops so is fully io determined
 [x] outputs/part1.v -> Latches in when the two input wires are both high
 [x] outputs/part2.v -> Some sort of lfsr or something? It cycles through 12 values
 [x] outputs/part3.v -> Another lfsr? This time 11 values.
 [x] outputs/part4.v -> Shift register with an 'enable' via muxes on Wire_9
 [ ] outputs/part5.v
 [ ] outputs/part6.v
 [ ] outputs/part7a.v
 [ ] outputs/part7b.v
 [ ] outputs/part7c.v
 [ ] outputs/part8.v
 [ ] outputs/part9a.v
 [ ] outputs/part9b.v
 [ ] outputs/part9c.v
 [ ] outputs/part9d.v
 [ ] outputs/part9e.v <- Should be easy
 [x] outputs/output_section.v
[ ] Draw out the circuit for outputs/part4.v

### Quality-of-life
[ ] Move wires and ports etc to be `Wire_<n>` and `<type>_<n>.<pin>`. The colon is annoying
```
"Wire_9", // Wire_9 is the 'S' signal for the Muxes, which is like the 'en' for the thing
```
