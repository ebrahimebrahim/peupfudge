#!/usr/bin/env python

from monte_carlo import *

#example tree to test this on:
eg = import_ability_tree("example.tree")

#example trainer that trains hauling three times and wound care four times
def eg_trainer(eg):
  h = eg.descendant('hauling')
  w = eg.descendant('wound care')
  for n in range(3):
    h.train()
  for n in range(4):
    w.train()

#thisruns 10000 trials of eg_trainer and stores the outcomes
outcomes = run_trials(eg,eg_trainer,10000)

#this will print out the average resulting tree
print mean_tree(eg,outcomes)

#this shows the probability distribution for the resulting level of "body"
show_histogram('body',outcomes)
