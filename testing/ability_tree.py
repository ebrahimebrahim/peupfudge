#!/usr/bin/env python

import random

class Node(object):
  def __init__(self, name, untrained_level=3, level=None):
    self.name = name
    self.untrained_level = untrained_level
    self.level = level if level is not None else untrained_level
    self.children_weights = []
    self.parent = None
  def add_child(self, child_node, weight=1):
    if not isinstance(child_node, self.__class__):
      raise TypeError("Child should be of type "+str(self.__class__)+".")
    child_node.parent = self
    self.children_weights.append((child_node, weight))
  def children(self):
    return [c for c,w in self.children_weights]
  def child_with_weight_by_name(self, name):
    try:
      return self.children_weights[[c.name for c,w in self.children_weights].index(name)]
    except ValueError:
      raise Exception(self.name+' has no child by the name '+name)
  def child(self, name):
    child, weight = self.child_with_weight_by_name(name)
    return child
  def weight_of(self, name):
    child, weight = self.child_with_weight_by_name(name)
    return weight
  def descendants(self):
    return self.children()+[d for c in self.children() for d in c.descendants()]
  def descendant(self, name):
    descendants = self.descendants()
    try:
      return descendants[[d.name for d in descendants].index(name)]
    except ValueError:
      raise Exception(self.name+' has no descendant by the name '+name)
  def is_skill(self):
    return not bool(self.children_weights)
  def own_weight(self):
    if self.parent is None:
      raise Exception(self.name+' has no weight because it has no parent.')
    return self.parent.weight_of(self.name)
  def __str__(self, indent=0):
    own_label = indent*'  ' + '['+(str(self.own_weight()) if self.parent else '-')+'] ' + self.name + ": " + str(self.level)
    children_labels = '\n'.join([c.__str__(indent+1) for c,w in self.children_weights])
    return own_label + ('\n' if not self.is_skill() else '') + children_labels
  def train(self, indirect = False):
    if not self.is_skill() and not indirect:
      raise Exception('Cannot directly train the attribute '+self.name+'.')
    self.level += 1
    if self.parent:
      w = float(self.own_weight())
      w_plus_n = sum(c.own_weight() for c in self.parent.children() if (c.level <= self.parent.level or c is self))
      p = w / w_plus_n #probability that the parent will increase
      if random.random() < p:
        self.parent.train(indirect=True)
    
  

eg = Node('level')
eg.add_child(Node('mind'))
eg.child('mind').add_child(Node('engineering', untrained_level=1))
eg.child('mind').add_child(Node('literacy'), weight=2)
eg.child('mind').add_child(Node('medicine', untrained_level=2))
eg.child('mind').child('medicine').add_child(Node('wound care', untrained_level=2))
eg.child('mind').child('medicine').add_child(Node('first aid'))
eg.add_child(Node('body'))
eg.child('body').add_child(Node('muscle strength'),weight=2)
eg.descendant('muscle strength').add_child(Node('hand-to-hand combat'))
eg.descendant('muscle strength').add_child(Node('hauling'))
eg.child('body').add_child(Node('climbing', untrained_level=2))
eg.child('body').add_child(Node('athletics'),weight=2)
eg.descendant('athletics').add_child(Node('swimming', untrained_level=2))
eg.descendant('athletics').add_child(Node('running', untrained_level=4))
