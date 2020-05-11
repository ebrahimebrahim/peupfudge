#!/usr/bin/env python

# this script is just me playing with the finite state machine idea
# - heim

import random, numpy

class Edge(object):
  def __init__(self, source, trigger, targets):
    self.trigger = trigger    # name of triggering event
    self.source  = source     # source Nodes
    self.targets = targets    # list of pairs (target Node,probability)

class Node(object):
  def __init__(self, name):
    self.name = name
    self.edges = [] #list of outgoing edges
  def add_edge(self, trigger, targets):
    self.edges.append(Edge(self,trigger,targets))

class Mfsm(object):
  def __init__(self, start_node):
    self.head = start_node
  def event(self, event_name):
    trigger_list = [edge.trigger for edge in self.head.edges]
    if event_name not in trigger_list:
      return self
    else:
      edge = self.head.edges[trigger_list.index(event_name)]
      c = 0
      r=random.random()
      for target in edge.targets:
        if r>=c and r<c+target[1]:
          self.head = target[0]
          return self
        c += target[1]
  def __str__(self):
    return self.head.name

f = Node("fine")
s = Node("scratched")
h = Node("hurt")
i = Node("incapactiated")
d = Node("dead")

f.add_edge("receive scratch",[(s,1.0)])
f.add_edge("receive hurt",[(h,1.0)])
f.add_edge("receive incap",[(i,1.0)])
f.add_edge("receive death",[(d,1.0)])
s.add_edge("receive hurt",[(h,1.0)])
s.add_edge("receive incap",[(i,1.0)])
s.add_edge("receive death",[(d,1.0)])
h.add_edge("receive incap",[(i,1.0)])
h.add_edge("receive death",[(d,1.0)])
i.add_edge("receive death",[(d,1.0)])

s.add_edge("receive scratch",[(s,0.75),(h,0.25)])
h.add_edge("receive scratch",[(h,0.90),(i,0.10)])
h.add_edge("receive hurt",[(h,0.6),(i,0.4)])
i.add_edge("receive scratch",[(i,0.95),(d,0.05)])
i.add_edge("receive hurt",[(i,0.75),(d,0.25)])
i.add_edge("receive incap",[(i,0.5),(d,0.5)])

hp=[d,i,h,s,f]
ld=["none","receive scratch","receive hurt","receive incap","receive death"]
def y(ld_in):
  data = []
  for n in range(10000):
    m=Mfsm(hp[4])
    for i in range(ld_in):
      m.event(ld[1])
    c = 0;
    while m.head.name != "dead":
      m.event(ld[1])
      c+=1
    data.append(c)
  return numpy.mean(data)
