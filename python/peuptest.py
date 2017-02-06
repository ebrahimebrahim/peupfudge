#!/usr/bin/env python

# Peuptest, a testing framework for Peupfudge.

from monte_carlo import *
import os, sys
import copy
import numpy

list_of_trees_to_test = ["example.tree"]
N = 1000

#---- DELETE THESE LINES WHEN DONE TESTING: (TODO)
eg = import_ability_tree("trees/example.tree")
#----

def main():
#  for t in list_of_trees_to_test:
#    test_tree(import_ability_tree(os.path.join("./trees/",t)))
#UNCOMMENT THE ABOVE AND DELETE THE pass WHEN DONE TESTING (TODO)
  pass



def trainer_from_sequence(seq):
  """Return a trainer function based on the given sequence of names"""
  def trainer(node):
    cost = 0
    for name in seq:
      try:
        cost += node.descendant(name).cost_to_train()
        node.descendant(name).train()
      except KeyError:
        raise Exception("Encountered unknown skill name \'"+name+"\' in training sequence "+seq)
    return cost
  return trainer

def test_tree(tree):
  maxtrain = 8
  skill_level_costs = {(skill.name,n) : numpy.mean(run_trials(tree,trainer_from_sequence(n*[skill.name]),num_trials=N,include_xpcosts=True)[1])
                       for skill in tree.skills() for n in range(1,maxtrain+1) }
  multipliers_by_skill = {skill.name : [(float(skill_level_costs[(skill.name,n+1)])/skill_level_costs[(skill.name,n)])
                                                for n in range(1,maxtrain)]
                      for skill in tree.skills() }
  return multipliers_by_skill


if __name__=="__main__":
  main()
