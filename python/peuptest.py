#!/usr/bin/env python

# Peuptest, a testing framework for Peupfudge.

from monte_carlo import *
import os, sys
import copy
import numpy
import random
import argparse

max_skill_level = 9
N = 100
percentiles = [0,25,50,75,100]
list_of_trees_to_test = ["barogna.tree", "example.tree", "mnb.tree", "morrowind.tree", "urw.tree"]

test2_explanation="""\n=== Explanation of discount factor and orders of relatedness ===
Consider the cost c of training a particular skill to be a function c(s,r) of
both the current level s of that skill and the levels r up to which we've trained
its related skills before. This can be measured by setting those related skills to
a fixed starting level (2 for the purposes of this test), training them up to level r,
and then asking how much it would cost to train the skill in focus up by one level from s.

The ratio c(s,r+1)/c(s,r), which we will call the discount factor, is what criterion 2
wants to be constant; test 2 gathers the distribution of this quantity.
We should expect different answers depending on how closely related of related skills
we train to get this statistic. A related skill of "order" 1 is a sibling skill or
a descendant thereof. A related skill of order 2 is an aunt skill, or descendant thereof."""

def main():
  parser = argparse.ArgumentParser(description="Run tests on xp cost formula and attribute bonus mechanic.")
  parser.add_argument("-t", "--tests", help="list of tests to run. e.g \"12\" to run tests 1 and 2.")
  args = parser.parse_args()
  if args.tests and '2' in args.tests:
    print test2_explanation+"\n\n\n"
  

  for t in list_of_trees_to_test:
    print "=== Report for tree "+t+" ===\n"
    test_tree(import_ability_tree(os.path.join("./trees/",t)), args.tests if args.tests else "12345")
    print "\n"

def test_tree(tree,tests):
  """Run specified tests on tree,
     analyze the collected data,
     and try to print some useful info.
     Specify tests in argument "tests", which is a string of numbers for test numbers.
  """

  tree_depth = max(len(skill.ancestors()) for skill in tree.skills())

  if '1' in tests:
    print "\n--- TEST 1 INFO ---"
    skill_level_costs = test1_data(tree)
    multipliers_by_skill = {skill.name : [(float(skill_level_costs[(skill.name,n+1)])/skill_level_costs[(skill.name,n)])
                                          for n in range(1,max_skill_level-1)]
                            for skill in tree.skills() }
    multipliers =  [multipliers_by_skill[skill.name][n] for skill in tree.skills() for n in range(max_skill_level-2)]
    print "Skill training xp cost ratio from one level to the next, percentiles "+str(percentiles)+" of distribution:"
    print ' '.join([str(round(p,2)) for p in numpy.percentile(multipliers,percentiles)])

  if '2' in tests:
    print "\n--- TEST 2 INFO ---"
  
    print "We list the percentiles "+str(percentiles)+" for the distribution of the discount factor (explained above).\n"
    orders = [1,2]
    o_DFlist = {o:[] for o in orders} # will map each order to list of measured discount factors over many skills over many conditions
    for skill in tree.skills():
      osr_DF = test2_data(tree,skill,orders)
      for o in orders:
        o_DFlist[o] += [osr_DF[k] for k in osr_DF.keys() if k[0]==o]
    o_DFpercentiles = {o:numpy.percentile(o_DFlist[o],percentiles) for o in orders}
    for o in orders:
      print "With respect to related skills of order "+str(o)+": "+' '.join([str(round(p,2)) for p in o_DFpercentiles[o]])
  
  if '3' in tests:
    print "\n--- TEST 3 INFO ---"
    orders = range(1,tree_depth+1)
    num_skills = [10, 25, 50, 100]
    print "When we train skills N times, its O^th ancestor tends to be this many levels higher than it:\n"
    row_format = "{:<5}" + "{:>5}" * (len(orders))
    print row_format.format(*(["N  O:"]+orders))
    for n in num_skills:
      print row_format.format(*([str(n)]+[str(round(test3(tree,n,o),1)) for o in orders]))
  
  if '4' in tests:
    print "\n--- TEST 4 INFO ---"
    g,c,p = test4(tree, portion=3, train_by=3)
    pcent_more = lambda a,b : str(int(round(100*(float(a)/float(b)-1))))
    print "To train a third of the skills from level 3 to 6:"
    print "  It costs the classmaker "+str(int(round(c)))+"xp."
    print "  It costs the generalist "+str(int(round(g)))+"xp, "+ pcent_more(g,c) +" percent more than the classmaker."
    print "  It costs the peuper     "+str(int(round(p)))+"xp, "+ pcent_more(p,c) +" percent more than the classmaker."
    
  if '5' in tests:
    print "\n--- TEST 5 INFO ---"
    start  = 3
    target = 6
    print "If we were to train all "+str(len(tree.skills()))+" skills from level "+str(start)+" to level "+str(target)+","
    print "then the distribution of resulting levels on the abilities is as described below."
    print "The first columns show the percentiles indicated at the top, and the number following an ability name is the mean.\n"
    print test5(tree, start, target, [1,5,25,75,95,99])
  

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

def random_trainer(n):
  """Return a trainer function that trains n random skills."""
  def trainer(node):
    cost = 0
    for i in range(n):
      skill = random.choice(node.skills())
      cost += skill.cost_to_train()
      skill.train()
    return cost
  return trainer

def nca_dist(l):
  """Return distance away of nearest common ancestor of given list l of skills."""
  assert(len(l)>=1)
  # ancestors of skill that *includes* self at beginning 
  anc = lambda s : [s]+s.ancestors()
  nca = [k for k in anc(l[0]) if all(k in anc(j) for j in l[1:])][0]
  # I have a particular idea in mind when I choose "min" below...
  # TODO: Is it correct?
  return min(anc(k).index(nca) for k in l)
  
def classmaker(tree,num_skills,cluster_size):
  """Return a random selection of num_skills skills from tree
     chosen in internally related clusters each consisting of
     cluster_size skills."""
  skillpool = set(tree.skills())
  assert cluster_size>0
  selection = []
  cluster = []
  for i in range(num_skills):
    if not cluster:
      skl = random.choice(list(skillpool))
      skillpool.remove(skl)
      cluster.append(skl)
    else:
      min_nca_dist = min(nca_dist([s]+cluster) for s in skillpool)
      skl = random.choice([s for s in skillpool if nca_dist([s]+cluster)==min_nca_dist])
      skillpool.remove(skl)
      cluster.append(skl)
    if i == num_skills-1 or len(cluster)==cluster_size:
      selection+=cluster
      cluster = []
  assert cluster==[]
  assert len(selection)==num_skills
  return selection

    
 
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
  return {(skill.name,n) : test1_run(tree, skill, n) for skill in tree.skills() for n in range(1,max_skill_level) }

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
  d_tree = mean_tree(d_tree, run_trials(d_tree, trainer_from_sequence(trainer), num_trials=N/3))
  if t-s==1:
    return d_tree.descendant(skill.name).cost_to_train()
  return expected_xpcost(d_tree, trainer_from_sequence((t-s)*[skill.name]), num_trials=N/3)
    
def test2_data(tree, skill, o_range=[1]):
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
       o can take on any value passed in the "o_range" argument, which is a list
       s can take on a low or a high value
       r ranges from r_start to 8

     Finally, a subtlety to heed:
      When we "set r" to some value to see it's effect on c_o(s,r), we are really *training* it
      up to that value from whatever it starts at in the tree, after *setting* it to r_start. 
      This is essential for test criterion (2), because it is in the process of training related skills
      that the mechanic is allowed to take effect.
  """
  r_start = 2 # level to start related skills at before training them up to various r's
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


def test3(tree, num_trains, order):
  """ Return average difference between levels of skills and levels of their ancestors of the given order.

      An ancestor of order 1 is a parent, order 2 a grandparent, etc.

      This will randomly train num_trains levels of skills.
      Then for each pair (s,a) for which 'a' is an ancestor of s of order 'order',
      subtract the level of s from the level of a.
      Average this quantity over all pairs (s,a), and over many of these random-training trials.
      Return this average.
  """
  if order <= 0:
    raise Exception("For test3 order should be 1 or greater.")
  tree_depth = max(len(skill.ancestors()) for skill in tree.skills())
  if order > tree_depth:
    raise Exception("test3 has no data to report on when the chosen order is greater than the depth of the tree.")
  mt = mean_tree(tree,run_trials(tree,random_trainer(num_trains),num_trials=N))
  return numpy.mean([(skill.ancestors()[order-1].level - skill.level) for skill in mt.skills() if len(skill.ancestors())>=order])
   
   
def test4(tree, portion=3, train_by=3):
  """ Return expected xp cost for generalist, classmaker, and peuper when training up the tree.
      A generalist will train skills randomly.
      A classmaker trains a cluster of related skills.
      A peuper trains two clusters of related skills.

      Args:
        tree:     (Node) the tree to work on
        portion:  (int) determines what portion of the skills are chosen for training.
                        for example portion=3 means 1/3 of skills get trained.
        train_by: (int) when training up a skill, this is how many levels it gets trained up.

      Returns: list of respective expected xp cost for generalist, classmaker, peuper.
  """
  d_tree = copy.deepcopy(tree) # dummy tree
  for skill in d_tree.skills():
    skill.level=3 # start each skill at 3
  num_skills = len(d_tree.skills())/portion
  assert num_skills>=1
  cluster_sizes = [1, num_skills, max(1,num_skills/2)] # the generalist, the classmaker, and the peuper

  def classmaker_trainer(cluster_size):
    def trainer(node):
      cost = 0
      seq = train_by*map(lambda s : s.name, classmaker(d_tree,num_skills, cluster_size))
      for name in seq:
          cost += node.descendant(name).cost_to_train()
          node.descendant(name).train()
      return cost
    return trainer

  return [expected_xpcost(d_tree, classmaker_trainer(cs), N*5) for cs in cluster_sizes]

def test5(tree, skills_start=3, skills_target=6, percentiles=[1,5,25,50,75,95,99]):
  """ Returns string showing tree that results if all skills are trained from level skills_start up to skills_target.
      The tree shown has the expected level of each individual ability next to it, along with a list
      of percentiles in the distribution consisting of the resulting level of that ability after each training trial.
  """
  d_tree = copy.deepcopy(tree)
  for skl in d_tree.skills():
    skl.level=skills_start
  assert (skills_target - skills_start) >= 0
  seq = (skills_target - skills_start) * [skl.name for skl in d_tree.skills()]
  return percentiles_tree(d_tree, run_trials(d_tree, trainer_from_sequence(seq), num_trials=10*N), percentiles)


if __name__=="__main__":
  main()
