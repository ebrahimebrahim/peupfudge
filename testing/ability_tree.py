#!/usr/bin/env python

import random, re

class Node(object):
  """Ability tree node class. AKA, ability tree, for the root node object.

  Attributes:
    name (str):      name of the ability
    level (int):     current level of ability
    weight (int):    weight of ability under its parent if it has one
    children (list): list of its children, which are themselves Node objects
    parent (Node):   parent of ability, if it has one

  __init__ arguments:
    name
    level (defaults to 3)
    weight (defaults to None, but is set to default of 1 if this node is made a child of another via add_child)
  """
  def __init__(self, name, level=3, weight=None):
    self.name = name
    self.level = level
    self.children = []
    self.weight = weight
    self.parent = None

  def add_child(self, child_node, weight=None):
    """Add child node to this node

       Args:
         child_node: Node object to add as child
         weight: weight to assign to added child

       Raises:
         TypeError: if the child is not a Node
    """
    if not isinstance(child_node, self.__class__):
      raise TypeError("Child should be of type "+str(self.__class__)+".")
    child_node.parent = self
    if weight:
      child_node.weight = weight
    elif not child_node.weight:
      child_node.weight = 1
    self.children.append(child_node)

  def child(self, name):
    """Access a child by its name"""
    try:
      return self.children[[c.name for c in self.children].index(name)]
    except ValueError:
      raise Exception(self.name+' has no child by the name '+name)
  def descendants(self):
    """Return list of all descendants of this Node (children, their children, etc.)"""
    return self.children+[d for c in self.children for d in c.descendants()]

  def descendant(self, name):
    """Access a descendant by name (a descendant need not be a direct child)"""
    descendants = self.descendants()
    try:
      return descendants[[d.name for d in descendants].index(name)]
    except ValueError:
      raise Exception(self.name+' has no descendant by the name '+name)

  def is_skill(self):
    """Return whether or not this ability is a skill"""
    return not bool(self.children)

  def __str__(self, indent=0):
    own_label = indent*'  ' + '['+(str(self.weight) if self.weight else '-')+'] ' + self.name + ": " + str(self.level)
    children_labels = '\n'.join([c.__str__(indent+1) for c in self.children])
    return own_label + ('\n' if not self.is_skill() else '') + children_labels

  def train(self, indirect = False):
    """Train this skill

       Args:
         indirect: (default=False) Set this to True to override the check that prevents training an attribute.

       Raises:
         Exception: if you try to train an attribute w/o setting indirect=True
    """
    if not self.is_skill() and not indirect:
      raise Exception('Cannot directly train the attribute '+self.name+'.')
    self.level += 1
    if self.parent:
      assert all(s.weight for s in self.parent.children) #all siblings should have a weight
      w = float(self.weight)
      w_plus_n = sum(s.weight for s in self.parent.children if (s.level <= self.parent.level or s is self))
      p = w / w_plus_n #probability that the parent will increase
      if random.random() < p:
        self.parent.train(indirect=True)




def import_ability_tree(filename):
  """Load ability tree from a file

     The syntax for the file is pretty strict at the moment,
     and the error checking is not perfect.
     Try doing "print" on a Node object to see what the syntax should be.
     Each indentation, for example, should be two spaces.

     Args:
       filename (str): path to text file containing ability tree

     Raises:
       various exceptions when it cannot parse things

     Returns: the root Node of the loaded ability tree
  """
  f = open(filename, 'r')
  lines = f.readlines()
  f.close()
  def parse_line(line):
    name_list = re.findall("(?<=]).+(?=:)", line)
    weight_list = re.findall("(?<=\[).+(?=\])", line)
    level_list = re.findall("(?<=:)[\d\s]+", line)
    if any(len(l)!=1 for l in [name_list,weight_list,level_list]):
      raise Exception("Could not parse the following line:\n"+line)
    return name_list[0].strip(), weight_list[0].strip(), level_list[0].strip()
  def indent_level(line):
    initial_spaces_list = re.findall("^[ ]+", line)
    if not initial_spaces_list:
      return 0
    assert(len(initial_spaces_list) == 1)
    n = len(initial_spaces_list[0])
    if n%2==1:
      raise Exception("Encountered indentation issue while parsing the following line:\n"+line)
    return n/2
  def node_from_lines(lines):
    assert(lines)
    i = indent_level(lines[0])
    assert(all(indent_level(line)>i for line in lines[1:]))
    name, weight, level = parse_line(lines[0])
    try:
      weight_int = int(weight)
    except ValueError:
      weight_int = None
    try:
      level_int = int(level)
    except ValueError:
      raise Exception("Could not parse ability level from the following line:\n"+lines[0])
    node = Node(name=name, level=level_int, weight=weight_int)
    child_lines = []
    for m in range(1,len(lines)):
      child_lines.append(lines[m])
      if m==len(lines)-1 or indent_level(lines[m+1])==i+1:
        node.add_child(node_from_lines(child_lines))
        child_lines=[]
    assert(not child_lines)
    return node
  return node_from_lines(lines)
  

eg = import_ability_tree("example.tree")
