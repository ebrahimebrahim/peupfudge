#!/usr/bin/env python

import copy
import numpy
import matplotlib.pyplot as plt
from ability_tree import *

def run_trials(node, trainer, num_trials=1000, include_xpcosts=False):
  """Run a training function many times on an ability tree, and return results.

     Args:
       node: initial ability tree, i.e. a root Node
       trainer: a function that takes a Node (ability tree) and does stuff to it
                (presumably by training a bunch of its skills)
                it should return the xp cost of the training, if you want to use that information
       num_trials: number of trials to run, defaults to 1000
       include_xpcosts: False by default. If enabled a list of xp costs is added as a return value.

     Returns the first or both of the following depending on include_xpcosts:
       outcomes as a dictionary with
         keys being names of abilities and
         values being lists of outcomes after applying the trainer function
       list of xp costs for each trial
  """
  outcomes = {d.name:[] for d in node.descendants()}
  xpcosts = []
  for n in range(num_trials):
    trial_node = copy.deepcopy(node)
    xpcosts.append(trainer(trial_node))
    for d in trial_node.descendants():
      outcomes[d.name].append(d.level)
  if include_xpcosts:
    return outcomes,xpcosts
  else:
    return outcomes

def expected_xpcost(node, trainer, num_trials=1000):
  """Run a training function many times on an ability tree, and return expected xp cost.

     Args are as in run_trials.
  """
  return numpy.mean(run_trials(node, trainer, num_trials, include_xpcosts=True)[1])

def mean_tree(node, outcomes):
  """Return a version of the ability tree whose ability levels are the average of those found in outcomes.
     The averages are rounded to the nearest tenth."""
  if set([d.name for d in node.descendants()]) != set(outcomes.keys()):
    raise Exception("It looks like the outcomes list you provided was meant for a different tree.")
  new_tree = copy.deepcopy(node)
  for ability_name in outcomes.keys():
    new_tree.descendant(ability_name).level = round(numpy.mean(outcomes[ability_name]),1)
  return new_tree

def show_histogram(ability_name, outcomes):
  """Show histogram of outcomes for given ability name"""
  l = outcomes[ability_name]
  plt.hist(l, normed=True, bins=range(min(l),max(l)+1));
  plt.show()

def percentiles_tree(node, outcomes, percentiles = [1,25,50,75,99]):
  """Return string showing tree with each ability preceded by a list of percentiles,
     and with mean replacing ability levels.

     Args:
       node: the ability tree, a Node
       outcomes: outcomes from a run_trials for that ability tree, a dict
       percentiles: a list of percentiles to display
  """
  #extra_info = {name : ' '.join([str(int(p)) for p in numpy.percentile(outcomes[name], percentiles)]) for name in outcomes.keys()}
  percentiles_format = ("{:>3}" * len(percentiles))
  extra_info = {name : percentiles_format.format( *[str(int(p)) for p in numpy.percentile(outcomes[name], percentiles)] )
                for name in outcomes.keys()}
  header = percentiles_format.format(*[str(p) for p in percentiles])+"\n\n"
  return header + mean_tree(node, outcomes).__str__(extra_info=extra_info)
