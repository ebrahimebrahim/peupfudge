#!/usr/bin/env python

# This script generates the learning curve plot that shows how experience gets mapped to ability level
# But not yet, it's unfinished.
# It's the start of an idea...
# Also, maybe this should be part of gen_numbers.py

from math import log


# b  = skill level base
# s  = xp scale factor
# s1 = xp per level for linear portion of the xp_to_level function
b = 1.85
s = 50.0 / pow(b,-2)
s1 = 25

xp2lvl = lambda x : log((x+(s1/log(b)))/s,b) - log(((s1/log(b)))/s,b)

def main():
  scriptname = os.path.basename(os.path.realpath(__file__))

if __name__ == "__main__":
  main()
