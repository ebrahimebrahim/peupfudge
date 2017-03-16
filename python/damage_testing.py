#!/usr/bin/env python

# Testing damage table stuff.
# -heim

from math import *
import numpy

adjs = ["terrible","poor", "mediocre", "fair", "good", "great","superb"]
adj_to_num = {"terrible":-3,"poor":-2, "mediocre":-1, "fair":0, "good":1, "great":2,"superb":3}

def show(b=1.3):
  assert(b>1)
  print "protection modifiers for when target is 1/f of the torso size, f running from 1 to 15:"
  prot = lambda f : int(round(log(f,b)))
  print [prot(f) for f in range(1,16)]
  step = (b-1)/2.0
  for c in numpy.arange(1,b+step,step):
    log_to_lin = lambda d : int(round(0.5*c*pow(b,d-1)))
    print "c = "+str(c)+" linearized damage from logarithmic:"
    print "  "+str([log_to_lin(d) for d in range(10)])
    for adj in adjs:
      print "  "+"A "+adj+" punch to guinea pig: " + str(log_to_lin(prot(4)+adj_to_num[adj]))
    for adj in adjs:
      print "  "+"A "+adj+" punch to arm: " + str(log_to_lin(prot(2)+adj_to_num[adj]))
    for adj in adjs:
      print "  "+"A "+adj+" punch to torso: " + str(log_to_lin(prot(1)+adj_to_num[adj]))
