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
eg2 = import_ability_tree("trees/example_test.tree")
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

def test2_run(tree, skill, s, t, o, r, r0):
  """Return data point for test criterion (2)

     Args:
       tree: tree to run test on
       skill: skill to train (as node)
       s:  starting level for skill
       t:  target level of skill
       o:  order of related skills to consider (see ability_tree.Node.related_skills to understand order)
       r:  level to train related skills up to beforehand, starting from r0
       r0: where to start related skills before training them up to r

     Returns:
       Expected xp cost of training skill from level s to level t,
       given that related skills up to order o have first been trained from r0 up to level r

     The way in which initial training of related skills is carried out is by taking the mean tree
     (see monte_carlo.mean_tree).
     Note that related skills of the specified order must first be *set* to a level of r0,
     in order to train them all up to r from the same starting conditions.
     While this may not reflect real peupfudge character development, it sufficies to provide
     a coherent metric for test criterion 2.
  """
  if r<r0:
    raise Exception("When call test2_run you cannot train related skills to r="+str(r)+" starting from r0="+str(r0)+".")
  d_tree = copy.deepcopy(tree) # d stands for "dummy"
  d_skill = d_tree.descendant(skill.name)
  d_skill.level = s
  trainer = [] # the training sequence for training related skills up to desired level of t + d
  for rel_skill in d_skill.related_skills(o):
    if rel_skill.name == d_skill.name:
      continue
    rel_skill.level = r0
    trainer += (r - r0) * [rel_skill.name]
  d_tree = mean_tree(d_tree, run_trials(d_tree, trainer_from_sequence(trainer), num_trials=N))
  if t-s==1:
    return d_skill.cost_to_train()
  return expected_xpcost(d_tree, trainer_from_sequence((t-s)*[skill.name]), num_trials=N)
    
def test2_data(tree, skill):
  """Return data set for test criterion (2)

     Given a tree and a skill in that tree (both Nodes), return a dict
       (o,s,r) --> DF
     where
       DF is the "Discount Factor,"
         which is defined to be DF = c_o(s,r+1) / c_o(s,r)
     where
       c_o(s,r) is the expected xp cost of training a skill at level s by one level
         given that its related skills of order o have been trained up to r from r_start
         (see definition of r_start in code)
     s is the level at which to start the given skill
     o is the order of relatedness of related skills
       (see ability_tree.Node.related_skills docstring for meaning of order)
     r is the level of related skills

     Perhaps the following is clearer:
       Fix a tree, and a skill in that tree.
       Fix an order o of related skills to consider for a given skill
       The (expected) xp cost of training a skill by one level can be considered as a function c_o(s,r)
       of the skill's current level s, and the level r of its related skills of order o.
       (Assuming we only care to vary those things here, of course)

     The range of (o,s,r)'s provided is small but reasonable:
       o can be 1 or 2
       s can take on a low or a high value
       r ranges from r_start to 8

     Finally, a subtlety to heed:
      When we "set r" to some value to see it's effect on c_o(s,r), we are really *training* it
      up to that value from whatever it starts at in the tree, after *setting* it to r_start. 
      This is essential for test criterion (2), because it is in the process of training related skills
      that the mechanic is allowed to take effect.
  """
  r_start = 2 # level to start related skills at before training them up to various r's
  o_range = [1,2]
  r_range = range(r_start, max_skill_level+1)
  min_s = 1
  max_s = max_skill_level-1
  s_range = [int(round(f*(max_s-min_s)+min_s)) for f in [0.2,0.8]]
  DF = {}
  for o in o_range:
    for s in s_range:
      c = {r:test2_run(tree,skill,s,s+1,o,r,r_start) for r in r_range}
      for r in r_range[0:-1]:
        DF[(o,s,r)] = float(c[r+1])/c[r]
  return DF


if __name__=="__main__":
  main()
