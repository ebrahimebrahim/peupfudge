#!/usr/bin/env python

# This provides the functions so you can play around with training sequences
# in an attempt to see what considerations go into optimizing for various goals.

from monte_carlo import *

# Starting ability tree to play this game on:
tree = import_ability_tree("trees/example.tree")

# XP budget to play with
budget = 3000

# A dictionary that converts one-character abbreviations to ability names
abbrev =\
{'e':'engineering',
 'l':'literacy',
 'w':'wound care',
 'f':'first aid',
 't':'hand-to-hand',
 'h':'hauling',
 'c':'climbing',
 's':'swimming',
 'r':'running'}

def trainer_from_sequence(seq):
  """Return a trainer function based on the given sequence of one character abbreviations"""
  def trainer(node):
    cost = 0
    for char in seq:
      try:
        cost += node.descendant(abbrev[char]).cost_to_train()
        node.descendant(abbrev[char]).train()
      except KeyError:
        raise Exception("Encountered unknown one-character abbreviation \'"+char+"\' in training sequence "+seq)
    return cost
  return trainer

def play_sequence(seq, num_trials=1000):
  """Play out a training sequence and print the results.

     Currently this relies on the following global variables:
       budget: the xp budget
       abbrev: the dictionary that maps one-character abbreviations
               to the skill names to which they correspond

     Args:
       seq: the training sequence, a string
       num_trials: number of trials to run, defaulting to 1000.

     Example:
       play_sequence("hhcch") # trains hauling twice, climbing twice, then hauling again.
                              # (assuming abbrev has h:hauling and c:climbing)
  """
  outcomes, xpcosts = run_trials(tree,trainer_from_sequence(seq),num_trials=num_trials,include_xpcosts=True)
  print percentiles(tree,outcomes) + "\n"
  print "Average XP cost: " + str(numpy.mean(xpcosts)) + "\n"
  print "Your XP budget: "+str(budget)
  over_percent = 100*float(len(filter(lambda x : x>budget,xpcosts)))/len(xpcosts)
  print "You went over your budget "+str(int(round(over_percent)))+"% of the time."
