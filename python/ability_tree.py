#!/usr/bin/env python

import random
import re
import gen_xptable as xptable

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

  def descendants(self, with_depth=False, start_depth=0):
    """Return list of all descendants of this Node (children, their children, etc.), including the node itself.
       If with_depth, False by default, is toggled on then the return will be a list of pairs (descendant, depth)
       where the root node has a depth of zero."""
    if with_depth:
      return [(self,start_depth)]+[(desc,dpth) for c in self.children for desc,dpth in c.descendants(with_depth=True, start_depth=start_depth+1)]
    else:
      return [self]+[d for c in self.children for d in c.descendants()]

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

  def skills(self):
    """Return descendants of this node that are skills, i.e. that do not themselves have children"""
    return [d for d in self.descendants() if d.is_skill()]

  def __str__(self, indent=0, extra_info=None):
    #extra_info gives a chance to display extra information from a str-->str, name |--> info, dict
    own_label = indent*'  ' + '['+(str(self.weight) if self.weight else '-')+'] ' + self.name + ": " + str(self.level)
    if extra_info:
      maxlen = max(len(s) for s in extra_info.values())
      own_label = extra_info[self.name] + (4+maxlen-len(extra_info[self.name]))*' ' + own_label
    children_labels = '\n'.join([c.__str__(indent+1,extra_info=extra_info) for c in self.children])
    return own_label + ('\n' if not self.is_skill() else '') + children_labels

  def ancestors(self):
    """Return list of ancestors, ordered starting from immediate parent."""
    return [self.parent]+self.parent.ancestors() if self.parent else []

  def related_skills(self, order=1):
    """Return a list of nearby skills in the tree related to this skill.
       
       Everything in the list returned is a skill.
       The argument "order" determines how far away to look from that skill.
       The only related skill of order 0 is this node itself (assuming it is a skill; otherwise include its descendants)
       Related skills of order 1 are sibling skills, and descendants thereof.
       Related skills of order 2 are cousin or aunt skills, and descendant thereof.
       And so on:
         Related skills of order n are descendant skills of the n^th ancestor

       What is returned is the list of related skills *up to* the given order
    """
    ancestors = self.ancestors()
    skills_only = lambda x : filter(lambda y : y.is_skill(), x)
    if order < 0:
      raise Exception("Related skills of order "+str(order)+"? Does not make sense.")
    if order > len(ancestors):
      return skills_only(ancestors[-1].descendants())
    if order == 0:
      return skills_only(self.descendants())
    assert order >= 1 and order <= len(ancestors)
    return skills_only(ancestors[order-1].descendants())

  def cost_to_train(self):
    """Return xp cost of training this skill
       
       This uses the actual xp table that goes into the manual, and has no more
       information to go off of than what is in that table.
       It will do all the rounding a player would do when reading off the table.
    """
    anc = self.ancestors()
    raw_attribute_bonus = sum( 1.0/pow(2,n)*a.level for n,a in enumerate(anc) ) / sum(1.0/pow(2,n) for n in range(len(anc)))
    attribute_bonus = min(xptable.alist, key = lambda x : abs(x-raw_attribute_bonus)) #round to closest available column in list
    return xptable.xp_cost(attribute_bonus, self.level)
    
  def probability_of_parent_increase(self):
    """Return probability that the parent will increase if this skill were trained, a float"""
    if not self.parent:
      raise Exception(self.name+' has no parent, so you cannot ask for the probability of parent increase')
    if not all(s.weight for s in self.parent.children):
      raise Exception(self.name+': could not compute probability of parent increase b/c some siblings seem not to have assigned weight')
    w = float(self.weight)
    w_plus_n = sum(s.weight for s in self.parent.children if (s.level <= self.parent.level or s is self))
    return w / w_plus_n

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
    if self.parent and random.random() < self.probability_of_parent_increase():
        self.parent.train(indirect=True)

  def tex(self, vert_spacing=0.85, horiz_spacing=3.5):
    """Return a tikz picture of this tree to be included in tex documents.
       The picture lists all skills down a column on the right, and extends ancestors to the left.
       Make sure you \\usepackage{tikz} in your tex document.

       Args:
         vert_spacing: (float or list) the vertical spacing in cm between skills
           if a single float is given then the  spacing is uniform
           if a list l of floats is given then the space between skills n and n+1 is l[n]
         horiz_spacing: (float or list) the spacing in cm between columns of the tree;
           if a single float is given then the spacing is uniform
           if a list l of floats is given then the space between columns n and n+1 is l[n]

       Returns:
         the tex as a string
    """
    undepth = lambda n : max(dpth for desc,dpth in n.descendants(with_depth=True)) 
    # (measures how deep the deepest child of a node is)
    maxdepth = undepth(self) # max undepth == max depth of course
    skills = [d for d in self.descendants() if undepth(d)==0]
    # these should be in the proper order to avoid crossing edges as much as possible
    # (given how Node.descendants works)

    if not hasattr(horiz_spacing, "__getitem__"):
      horiz_spacing = maxdepth*[horiz_spacing]
    if not hasattr(vert_spacing, "__getitem__"):
      vert_spacing = (len(skills)-1)*[vert_spacing]
      
    def how_far_down(n):
      if undepth(n) == 0: # the base case for how_far_down is skills
        row = skills.index(n)
        return sum(vert_spacing[:row])
      #for everything else, we base it on how its children are positioned
      assert(all(undepth(c)<undepth(n) for c in n.children))
      # ... obviously the children are less undeep right?
      children_positions = [how_far_down(c) for c in n.children]
      return (min(children_positions) + max(children_positions))/2.
    def how_far_over(n):
      column = maxdepth - undepth(n) #columns are 0, 1, ..., maxdepth
      return sum(horiz_spacing[:column])
        

    tex = """\\tikzset{
  treenode/.style = {shape=rectangle, rounded corners, top color=white, draw},
  attribute/.style     = {treenode, font=\\ttfamily\\normalsize, bottom color=blue!30},
  skill/.style         = {treenode, font=\\ttfamily\\normalsize, bottom color=red!20, right},
  weight/.style = {pos=0.5, shape=circle, scale=1, minimum height=1, inner sep=1pt, fill=white, font=\\scriptsize, draw}
}
\\begin{tikzpicture}\n"""
    def nodestr(node):
      nodestr  = '(' + str(how_far_over(node)) + ',' + str(-how_far_down(node)) + ') '
      nodestr += 'node ['+('skill' if node.is_skill() else 'attribute')+'] '
      nodestr += '(' + node.name + ') '
      nodestr += '{' + node.name + ' ' + str(node.level) + '} '
      return nodestr
    tex += "\\draw\n"
    for n in self.descendants():
      tex += "  "+nodestr(n)+"\n"
    tex += ";\n"
    for n in self.descendants():
      for c in n.children:
        tex += "\\draw[-{latex}] (" + n.name + ") -- (" + c.name + ".west)"
        tex += "  node[weight]{" + str(c.weight) + "};\n"
    tex += "\\end{tikzpicture}"
    return tex



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
  

