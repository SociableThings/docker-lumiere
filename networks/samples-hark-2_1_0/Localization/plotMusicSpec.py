#!/usr/bin/env python
import pylab
import sys

lines = [line.split()[2:] for line 
         in open(sys.argv[1]) if "MUSIC" in line]
spec = pylab.array([map(float, line) for line in lines]).transpose()
pylab.imshow(spec, interpolation="nearest", aspect="auto")
pylab.ylabel("Direction")
pylab.xlabel("Time [frame]")
pylab.colorbar()
pylab.show()
