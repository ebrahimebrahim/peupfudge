#!/usr/bin/env python

import ability_tree as T
import random
t=T.import_ability_tree("trees/combat_test.tree")


dF = lambda n : sum(random.choice([-1,0,1]) for i in range(n))


class Attack(object):
  def __init__(self,verb,weapon,hit_ab,dmg_ab,def_ab,abs_ab):
    self.verb=verb
    self.weapon = weapon
    self.hit_ab=hit_ab
    self.dmg_ab=dmg_ab
    self.def_ab=def_ab
    self.abs_ab=abs_ab


#actually this should inherit from a more generic Item class
class Item(object):
  
  def __init__(self,name,dmg):
    self.name = name


punch = Attack("punch",None,"punching","strength","brawl defending","constitution")
kick = Attack("kick",None,"kicking","strength","brawl defending","constitution")

#could have one of these for each type of creaturs:
wound_zones = {"head":5,"chest":6,"stomach":6,"l_arm":5,"r_arm":5,"l_leg":7,"r_leg":7, "neck":1}
def random_target(wound_zones):
  r = random.randrange(sum(wound_zones.values()))
  c = 0
  for z in wound_zones.keys():
    if r >= c and r < c+wound_zones[z]:
      return z
    c += wound_zones[z]
  

#represents a wound level on a particular body part
class WoundLevel(object):
  def __init__(self):
    self.num_scratches = 0
    self.num_hurts = 0
    self.incapped = False
    self.dead = False
  def scratch(self):
    if self.num_scratches < 3:
      self.num_scratches += 1
    else:
      self.hurt()
  def hurt(self):
    if self.num_hurts < 2:
      self.num_hurts += 1
    else:
      self.incap()
  def incap(self):
    if not self.incapped:
      self.incapped=True
    else:
      self.die()
  def die(self):
    self.dead=True
  def __str__(self, name='it'):
    intro = name + " is"
    details = str(self.num_scratches)+" scratches and "+str(self.num_hurts)+" hurts"
    if self.dead:
      return intro + " dead"
    elif self.incapped:
      return intro + " incapacitated (with "+details+")"
    elif self.num_scratches==0 and self.num_hurts==0:
      return intro + " fine"
    else:
      return name + " has " + details

class Character(object):
  
  def __init__(self,name):
    self.name = name
    self.tree = T.import_ability_tree("trees/combat_test.tree")
    self.inventory = []
    self.wounds = {}
    for body_part in wound_zones.keys():
      self.wounds[body_part] = WoundLevel()
  def report_wounds(self):
    for body_part in self.wounds.keys():
      print self.wounds[body_part].__str__(body_part)
  def is_alive(self):
    return all(not self.wounds[body_part].dead for body_part in ["head","neck","chest"])
  def attack(self, defender, attack):
    M  = self.tree.descendant(attack.hit_ab).level
    Mp = defender.tree.descendant(attack.def_ab).level
    dA  = self.tree.descendant(attack.dmg_ab).level
    dAp = defender.tree.descendant(attack.abs_ab).level
    rp = (dF(2)+M) - (dF(2)+Mp) #relative performance
    Delta = dA - dAp #damage factor
    dmg = 0; verb = "misses"
    if rp<0:
      return verb
    elif rp==0:
      dmg = 0.5 * (Delta + dF(1))
      verb="grazes"
    elif rp>0:
      dmg = 2*rp + Delta + dF(1)
      verb="hits"
    target = random_target(wound_zones)

    woundword="nothing"
    if dmg < 1:
      pass
    elif dmg < 5:
      woundword = "scratching"
      defender.wounds[target].scratch()
    elif dmg < 9:
      woundword = "hurting"
      defender.wounds[target].hurt()
    else:
      woundword = "incapacitation"
      defender.wounds[target].incap()

    return self.name+" "+verb+" "+defender.name+" in the "+target+", resulting in "+woundword


A = Character("Alice")
B = Character("Bob")
rounds = 0
while A.is_alive() and B.is_alive():
  rounds += 1
  A.attack(B,punch)
  B.attack(A,punch)
print rounds
