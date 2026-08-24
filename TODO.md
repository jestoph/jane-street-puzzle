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

### Basic valication
[x] Check all cells are showing ports correctly - they all look OK
[ ] Check stats
[ ] Check can read circuit
[ ] Check can simplify - some errors I'll need to resolve
