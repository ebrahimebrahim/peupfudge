#!/usr/bin/env python

#This file is where I am testing out ability tree stuff.
# -heim

from monte_carlo import *

#example tree to test things on:
eg = import_ability_tree("example.tree")

#example trainer that trains hauling three times and wound care four times
def trainer1(eg):
  h = eg.descendant('hauling')
  w = eg.descendant('wound care')
  for n in range(3):
    h.train()
  for n in range(3):
    w.train()

#alternating version of that
def trainer2(eg):
  h = eg.descendant('hauling')
  w = eg.descendant('wound care')
  h.train()
  w.train()
  h.train()
  w.train()
  h.train()
  w.train()

#train each skill thrice
def trainer3(eg):
  for d in eg.descendants():
    if d.is_skill():
      d.train()
      d.train()
      d.train()

#repeat trainer3 10 times
def trainer4(eg):
  for n in range(10):
    trainer3(eg)

o = run_trials(eg, trainer4, num_trials=10000)
show_percentiles(eg, o)
