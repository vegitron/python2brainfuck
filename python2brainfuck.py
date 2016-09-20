#!/usr/bin/env python
import sys
from p2bf.builder import BFBuild

verbose = False
if len(sys.argv) == 1:
    print "Usage: python2brainfuck.py [-v] path"
    sys.exit(1)
if len(sys.argv) == 3:
    verbose = True
    path = sys.argv[2]
else:
    path = sys.argv[1]

py = open(path)
program = ""
buff = py.read(1024)
pparts = []
while (buff):
    pparts.append(buff)
    buff = py.read(1024)

program = "".join(pparts)

BFBuild(program, verbose=verbose).emit_bf()

