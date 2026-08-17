

### Starting ideas
[x] Start trying to extract the network
[x] Extract all unique cells to individual gds and svg using a makefile
[x] Work out coordinate system of the file
[x] Work out how to filter on global coords rather than local - maybe flatten all top cells, and do it by bounding box?
[x] Turn this into a proper repo on my github
[x] Create a realtime-updating svg viewer? - No, not needed. Chrome does a good-enough job

### GDS Tooling
[ ] Find a local GDS viewer - could I use Raylib + voxels? Probably not a good idea but ....
  [x] Start gds viewer in raylib - steal an example
  [x] Fix orthographic view in examples - relies on rcamera and possibly rmath, can probably copy-paste
  [x] Draw up my understanding of raylib camera perspectives (first/third person, orthographic) in xcalidraw
  [ ] Get standard camera movements working -
    [ ] Pan
    [ ] Zoom
    [ ] Drag/rotate
  [ ] Work out how to highlight a cell - there's a voxel example that does this.
  [ ] Try to place some elements for a small cell

### Understanding the network
[x] Try to understand individual cells
  [x] Look at circuit elements made by cells.py
  [x] Work out how to show labels (maybe convert to text?) and add them to cells.py - Was done already in svg function
  [x] Look at obscured labels under PWR and GND labels
  [x] Read the manual - https://sky130-unofficial.readthedocs.io/en/latest/
  [x] Can I map labels on io ports to geometry?
[x] Draw up my understanding of gds in xcalidraw - not necessary, it's all spelled out in the docs
[ ] Map out the graph
  [x] Try to find a single example of a circuit element connected to a wire and write it to a gds
  [x] Build a gds of all connected, useful/interesting components
      - Got one working but with 'directional' artifacts. The naive algorithm isn't the best
  [x] Use a proper flood fill or graph traversal algorithm - layer connection worked fine
  [x] Fix bounding box issue
  [x] Work out how to take multiple distinct wires and convert into a single wire
  [ ] Add inputs and outputs to the circuit descriptions - maybe `x<1` or `x>99` would do the job? Honestly some xy coords on the rendering would be so nice
  [ ] Try to build a dot file (might need to give each pad a unique name like `AND:123:A -> MUX:7:Q` or something like that)
  [ ] Understand via scripts the following elements:
     [x] Comparitor
     [x] Shift Register 1
     [ ] Shift Register 2 <- There's some bug here, I have two wires connected to only one component
     [ ] Adder <- not feeling confident this will work
[ ] What are boundaries?
[ ] Why does the text file have more types?
[ ] Add all cell elements to my sim
  [ ] `a21bo_2`
  [ ] `a21boi_2`
  [ ] `a21o_2`
  [ ] `a31o_2`
  [ ] `o21bai_2`
  [ ] `and2_2`
  [ ] `and3_2`
  [ ] `and4bb_2`
  [ ] `clkbuf_16`
  [ ] `mux2_1`
  [ ] `nand2_2`
  [ ] `nor2_2`
  [ ] `or2_2`
  [ ] `xnor2_2`
  [ ] `xor2_2`
  [ ] `dfrtp_2`
  [ ] `decap_3`
  [ ] `tapvpwrvgnd_1`
