#!/usr/bin/env python

# This script generates the learning curve plot that shows how experience gets mapped to ability level

from math import log


smoothstep = lambda x : 0 if x <=0 else (1 if x >= 1 else (3*pow(x,2)-2*pow(x,3)))
# return a function that takes the value of f1(x) for x<=s, f2(x) for x>=e, and smoothly transitions in between
interpolate_funs = lambda f1,f2,s,e : (
                     lambda x : (1-smoothstep((x-s)/(e-s)))*f1(x) + smoothstep((x-s)/(e-s))*f2(x)
                   )

# b = skill level base
# s = xp scale factor
# d = discount factor
b = 1.85
s = 50.0 / pow(b,-2)
d = 1.35/b

# s1 = xp per level for linear portion of the xp_to_level function
s1 = 25
start_transition = s1
end_transition = s1 + 100

experience_to_level = interpolate_funs(lambda x : (x/s1), lambda xp : log(x/s,b), start_transition, end_transtion)

def main():
  scriptname = os.path.basename(os.path.realpath(__file__))

if __name__ == "__main__":
  main()
