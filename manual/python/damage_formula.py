#!/usr/bin/env python

# Testing damage table stuff.

from math import *
import numpy


adjs = ["abysmal","terrible","poor", "mediocre", "fair", "good", "great","superb","legendary", "5", "8"]
adj_to_num = {"abysmal":-4,"terrible":-3,"poor":-2, "mediocre":-1, "fair":0, "good":1, "great":2,"superb":3,"legendary":4, "8":8, "5":5}
protection = lambda f,b : int(round(log(float(f),b))) # protection modifier due to being size f*baseline size
linearized_dmg = lambda d,c,b : int(round(0.5*c*pow(b,d-1)))

def show(b):
  assert(b>1)
  print "protection modifiers for when target is 1/f of the torso size, f running from 1 to 15:"
  print [protection(f,b) for f in map(lambda x:1.0/x,range(1,16))]
#  step = (b-1)/2.0
#  for c in numpy.arange(1,b+step,step):
  c = 1+(b-1)/2
  print "c = "+str(c)+" linearized damage from logarithmic:"
  print "  "+str([linearized_dmg(d,c,b) for d in range(10)])
  for adj in adjs:
    print "  "+"A "+adj+" punch to guinea pig: " + str(linearized_dmg(protection(0.25,b)-adj_to_num[adj],c,b))
  for adj in adjs:
    print "  "+"A "+adj+" punch to arm: " + str(linearized_dmg(protection(0.5,b)-adj_to_num[adj],c,b))
  for adj in adjs:
    print "  "+"A "+adj+" punch to torso: " + str(linearized_dmg(protection(1,b)-adj_to_num[adj],c,b))

# These are the choices of b and c that we've decided on:
b = 1.285
c = 1.1425
