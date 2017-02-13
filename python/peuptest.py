#!/usr/bin/env python

# Peuptest, a testing framework for Peupfudge.

from monte_carlo import *
import os, sys
import copy
import numpy

max_skill_level = 9
N = 200

list_of_trees_to_test = ["example.tree"]

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
  """Run all tests on tree,
     analyze the collected data,
     and try to print some useful info

     (This will soon change:
      Instead of printing out information, it will return it in some form,
      so that main() can do the work of producing a cumulative report for all trees)
  """

  # test 1:
  skill_level_costs = test1_data(tree)
  multipliers_by_skill = {skill.name : [(float(skill_level_costs[(skill.name,n+1)])/skill_level_costs[(skill.name,n)])
                                        for n in range(1,max_skill_level-1)]
                          for skill in tree.skills() }
  multipliers =  [multipliers_by_skill[skill.name][n] for skill in tree.skills() for n in range(max_skill_level-2)]
  min_mult = round(min(multipliers),2)
  max_mult = round(max(multipliers),2)
  print "Skill training xp cost ratio from one level to the next:"
  print "  ranges from " + str(min_mult) + " to " + str(max_mult)

  # test 2:
  for skill in tree.skills():
    pass
    #PEUP TODO
 
def test1_run(tree, skill, n):
  """Return data point for test criterion (1)

     Args:
       tree: tree to run test on
       skill: skill to train (as node)
       n: number of times to train that skill

     Returns:
       Expected xp cost to train given skill n times
  """
  return expected_xpcost(tree,trainer_from_sequence(n*[skill.name]),num_trials=N)

def test1_data(tree):
  """Return data set for test criterion (1)

     Returns a dictionary mapping (s, n) --> c
       where s is a skill name, ranging over all skills in the tree
             n is the number of times to train that skill, ranging from 1 to max_skill_level
             c is the expected xp cost for that training
  """
  return {(skill.name,n) : test1_run(tree, skill.name, n) for skill in tree.skills() for n in range(1,max_skill_level) }

def test2_run(tree, skill, s, t, o, r):
  """Return data point for test criterion (2)

     Args:
       tree: tree to run test on
       skill: skill to train (as node)
       s: starting level for skill
       t: target level of skill
       o: order of related skills to consider (see ability_tree.Node.related_skills to understand order)
       r: level to train related skills up to beforehand

     Returns:
       Expected xp cost of training skill from level s to level t,
       given that related skills up to order o have first been trained up to level r

     Raises Exception:
       If a related skill happens to start at a level higher than r

     The way in which initial training of related skills is carried out is by taking the mean tree.
     (see monte_carlo.mean_tree)
  """
  d_tree = copy.deepcopy(tree) # d stands for "dummy"
  d_skill = d_tree.descendant(skill.name)
  d_skill.level = s
  trainer = [] # the training sequence for training related skills up to desired level of t + d
  for rel_skill in d_skill.related_skills(o):
    if rel_skill.name == d_skill.name:
      continue
    if r - (rel_skill.level) < 0:
      raise Exception("Warning: while running test 2, examining the skill \""+d_skill.name+"\", "
                      "an attempt was made to train the related skill \""+rel_skill.name+"\" "
                      "to level "+str(r)+". But it *starts* at level "+str(rel_skill.level)+".")
    trainer += (r - rel_skill.level) * [rel_skill.name]
  d_tree = mean_tree(d_tree, run_trials(d_tree, trainer_from_sequence(trainer), num_trials=N))
  return expected_xpcost(d_tree, trainer_from_sequence((t-s)*[skill.name]), num_trials=N)
    
def test2_data(tree, skill):
  # TODO figure out what data to collect here...
  # note that at the moment, this raises the exception that test2_run can raise.
  ss = [3,max_skill_level-3]
  t_minus_s = 2
  os = [1,2]
  r_minus_ss = [-2,-1,0,1,2]
  return {(s,t_minus_s+s,o,r_minus_s+s):test2_run(tree, skill, s, t_minus_s+s, o, r_minus_s+s) for s in ss for o in os for r_minus_s in r_minus_ss}



if __name__=="__main__":
  main()
