
## The Jane Street Reverse Engineering Challenge

This repo holds the terrible code I wrote for the Jane Street Reverse Engineering Challenge in August/September of 2026.

I would not recommend you use any of it as it's quite custom to this specific challenge, and my peculiar workflows,
but I thought it could be interesting as a companion piece to my blog about this challenge.

### Requirements
* Python - At a minimum you will require `gdstk` and `z3` installed with `pip` or `uv` or whatever you like.
* iverilog - for running the simulations/testbenches
* Surfer or some other waveform viewer
* I used `https://gds-viewer.tinytapeout.com/` for viewing GDS files. This is not ideal as it's in a browser, but I didn't
  find an alternative

### Structure

The flow of work looks something like:

1. Analysis work - This is done with `stats.py` which takes various counts of objects in the file and `cells.py` which
   extracts each component in the file in to a few formats -
    a. Full svgs and gds files
    b. Reduced forms with only elements I care about
2. Extracting a network of wire segments and elements from the GDS - this is done with `network.py`. For the warmup work it
   takes a few seconds. For the larger puzzle I believe around 55 to 60s. This is probably wholly unnecessary but I
   attempted some caching and improvements and it broke everything so I gave up.
3. Turning a graph of wire segments into a canonical set of wires and nodes, then writing them in to a bunch of formats -
   this is done by `simplify.py`. It also adds aliases to wires that I really care about (typically busses between sections)
   The formats include -
    a. Json
    b. Verilog
    c. Json & Verilog for subsections of the circuits (all hand-specified)
4. A small step for rewriting verilog modules in to simpler forms called `rewrite-module.py`
5. A series of solver scripts for various subsections of the circuits, all called `solver*.py`. These are a mix of hand-
   extracted verilog translated to z3, as well as some best-guesses of behaviour which turned out to be good enough.


There are also some driver programs named `test-*.py` and some testing scripts called `check-*.py` which generally check
whatever they are named. One of these actually found a small bug (an unconnected wire) in the circuit!

