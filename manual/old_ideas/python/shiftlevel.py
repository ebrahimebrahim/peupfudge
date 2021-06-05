#!/usr/bin/env python

# This script shifts the levels of all the abilities in all the trees in the trees/ directory
# We shouldn't ever need to use it again...
SHIFT_AMOUNT = -5

from ability_tree import *
import os, glob

os.chdir("trees/")
for filename in glob.glob("*.tree"):
  t = import_ability_tree(filename)
  for a in t.descendants():
    a.level += SHIFT_AMOUNT
  f = open(filename,'w')
  f.write(str(t)+'\n')
  f.close()
