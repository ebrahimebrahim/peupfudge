#!/usr/bin/env python

import copy
import numpy
import matplotlib.pyplot as plt
from ability_tree import *

def run_trials(node, trainer, num_trials=1000):
  """Run a training function many times on an ability tree, and return results.

     Args:
       node: initial ability tree, i.e. a root Node
       trainer: a function that takes a Node (ability tree) and does stuff to it
                (presumably by training a bunch of its skills)
       num_trials: number of trials to run, defaults to 1000

     Returns:
       outcomes as a dictionary with
         keys being names of abilities and
         values being lists of outcomes after applying the trainer function
  """
  outcomes = {d.name:[] for d in node.descendants()}
  for n in range(num_trials):
    trial_node = copy.deepcopy(node)
    trainer(trial_node)
    for d in trial_node.descendants():
      outcomes[d.name].append(d.level)
  return outcomes

def mean_tree(node, outcomes):
  """Return a version of the ability tree whose ability levels are the average of those found in outcomes"""
  if set([d.name for d in node.descendants()]) != set(outcomes.keys()):
    raise Exception("It looks like the outcomes list you provided was meant for a different tree.")
  new_tree = copy.deepcopy(node)
  for ability_name in outcomes.keys():
    new_tree.descendant(ability_name).level = numpy.mean(outcomes[ability_name])
  return new_tree

def show_histogram(ability_name, outcomes):
  """Show histogram of outcomes for given ability name"""
  l = outcomes[ability_name]
  plt.hist(l, normed=True, bins=range(min(l),max(l)+1));
  plt.show()

def show_percentiles(node, outcomes, percentiles = [1,25,50,75,99]):
  """Show tree with each ability preceded by a list of percentiles, and with mean replacing ability levels.

     Args:
       node: the ability tree, a Node
       outcomes: outcomes from a run_trials for that ability tree, a dict
       percentiles: a list of percentiles to display
  """
  extra_info = {name : str([int(p) for p in numpy.percentile(outcomes[name], percentiles)]) for name in outcomes.keys()}
  print mean_tree(node, outcomes).__str__(extra_info=extra_info)
