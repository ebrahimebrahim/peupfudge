#!/usr/bin/env python

import ability_tree as T
import numpy, math, copy, sys, random

dF = lambda n : sum(random.choice([-1,0,1]) for i in range(n))

class Attack(object):
  def __init__(self,verb,weapon,hit_ab,dmg_ab,def_ab,abs_ab):
    self.verb=verb
    self.weapon = weapon
    self.hit_ab=hit_ab
    self.dmg_ab=dmg_ab
    self.def_ab=def_ab
    self.abs_ab=abs_ab


class Item(object):
  
  def __init__(self,name,dmg):
    self.name = name


punch = Attack("punch",None,"punching","strength","brawl defending","constitution")
kick = Attack("kick",None,"kicking","strength","brawl defending","constitution")

#the first thing in the following tuple is a dict of wound zones with sizes.
#the second thing is a dict mapping each ability to a list of lists of body parts,
#indicating that you need all of the body parts in at least one of those lists in order to use that ability.
#there is also one extra ability in there that is not really an ability called "not being dead"
#(it indicates the critical body parts needed for being alive)
wound_zones_human = ( {"head":4,"chest":6,"stomach":6,"l_arm":5,"r_arm":5,"l_leg":7,"r_leg":7, "neck":1},
                      { "not being dead"  : [['head','chest','neck']],
                        "brawl defending" : [['l_leg','r_leg','l_arm','r_arm']],
                        "punching"        : [['l_arm'],['r_arm']],
                        "kicking"         : [['l_leg','r_leg']]
                      }
                    )
wound_zones_blob  = ( {"blob":1},
                      { "not being dead"  : [['blob']],
                        "brawl defending" : [['blob']],
                        "punching"        : [['blob']],
                        "kicking"         : [['blob']]
                      }
                    )
def random_target(wound_zones):
  r = random.randrange(sum(wound_zones[0].values()))
  c = 0
  for z in wound_zones[0].keys():
    if r >= c and r < c+wound_zones[0][z]:
      return z
    c += wound_zones[0][z]

#represents a wound level on a particular body part
class WoundLevel(object):
  def __init__(self, max_scratches=24, max_hurts=16):
    self.max_scratches = max_scratches
    self.max_hurts     = max_hurts
    self.num_scratches = 0
    self.num_hurts = 0
    self.incapped = False
    self.dead = False
  def scratch(self):
    if self.num_scratches < self.max_scratches:
      self.num_scratches += 1
    else:
      self.hurt()
  def hurt(self):
    if self.num_hurts < self.max_hurts:
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
  
  def __init__(self,name,wound_zones=wound_zones_human):
    self.name = name
    self.tree = T.import_ability_tree("trees/combat_test.tree")
    self.wound_zones=wound_zones
    self.wounds = {}
    for body_part in wound_zones[0].keys():
      self.wounds[body_part] = WoundLevel(24/len(wound_zones[0]),16/len(wound_zones[0]))
  def report_wounds(self):
    for body_part in self.wounds.keys():
      print self.wounds[body_part].__str__(body_part)
  def is_alive(self):
    return any(all(not self.wounds[body_part].dead for body_part in body_part_list) for body_part_list in self.wound_zones[1]['not being dead'])
  def injury_penalty(self,ability_name): 
    or_reqs = self.wound_zones[1][ability_name]
    out = lambda req : self.wounds[req].dead  or self.wounds[req].incapped
    if all(any(out(req) for req in and_reqs) for and_reqs in or_reqs):
      return 4
    penalty_from_hurts = lambda x : int(round(x*1.75/self.wounds.values()[0].max_hurts))
    return min(max(penalty_from_hurts(self.wounds[req].num_hurts) for req in and_reqs) for and_reqs in or_reqs)
  def attack(self, defender, attack):
    self_injpen = self.injury_penalty(attack.hit_ab)
    def_injpen  = defender.injury_penalty(attack.def_ab)

    M  = self.tree.descendant(attack.hit_ab).level - self_injpen
    Mp = defender.tree.descendant(attack.def_ab).level - def_injpen

    injpen_words = ""
    if self_injpen > 0:
      injpen_words += self.name + " has trouble with "+attack.hit_ab+" ("+str(-self_injpen)+"). "
    if defender.injury_penalty(attack.def_ab)>0:
      injpen_words += defender.name + " has trouble with "+attack.def_ab+" ("+str(-def_injpen)+"). "

    dA  = self.tree.descendant(attack.dmg_ab).level
    dAp = defender.tree.descendant(attack.abs_ab).level
    rp = (dF(2)+M) - (dF(2)+Mp) #relative performance
    Delta = dA - dAp #damage factor
    dmg = 0; verb = "misses"
    if rp<0:
      return injpen_words + self.name + " " + verb + " with a " + attack.verb + "."
    elif rp==0:
      dmg = 0.5 * (Delta + dF(1))
      verb="grazes"
    elif rp>0:
      dmg = 2*rp + Delta + dF(1)
      verb="hits"
    target = random_target(defender.wound_zones)

    woundword="nothing"
    if dmg < 1:
      pass
    elif dmg < 4:
      woundword = "scratching"
      defender.wounds[target].scratch()
    elif dmg < 7:
      woundword = "hurting"
      defender.wounds[target].hurt()
    elif dmg < 15:
      woundword = "incapacitation"
      defender.wounds[target].incap()
    else:
      woundword = "death"
      defender.wounds[target].die()

    return injpen_words+self.name+" "+verb+" "+defender.name+\
           " in the "+target+" with a "+attack.verb+\
           ", resulting in "+woundword+". "+\
           defender.wounds[target].__str__("It")+"."


A = Character("Alice")
A.tree.descendant("kicking").train()
A.tree.descendant("kicking").train()
B = Character("Bob")

def battle_data(char1,char2):
  """ Return mean number of rounds and char1 win rate for battle between these characters. """
  data=[]
  for i in range(100):
    A=copy.deepcopy(char1)
    B=copy.deepcopy(char2)
    rounds = 0
    while A.is_alive() and B.is_alive():
      rounds += 1
      attacks = [punch,kick]
      A.attack(B,sorted(attacks,key=lambda a : (A.injury_penalty(a.hit_ab),-A.tree.descendant(a.hit_ab).level))[0])
      B.attack(A,sorted(attacks,key=lambda a : (B.injury_penalty(a.hit_ab),-B.tree.descendant(a.hit_ab).level))[0])
    data.append((rounds,A.is_alive()))
  return numpy.mean([d[0] for d in data]) , len(filter(lambda d : d[1],data))/float(len(data))

print ""
print "Charl vs Dennis"
print "Increasing strength of Charl along columns. Increasing punching skill of Charl down rows."
print "Top left is equally matched."
print "Entries have the form [win rate] ([mean number of rounds])."
for punching_train in range(4):
  for strength_train in range(4):
    C=Character("Charl")
    D=Character("Dennis")
    for i in range(punching_train):
      C.tree.descendant("punching").train()
    for i in range(strength_train):
      C.tree.descendant("strength").train()
    rounds, winrate = battle_data(C,D)
    sys.stdout.write(str(int(round(100*winrate)))+" ("+str(int(rounds))+")\t\t")
  sys.stdout.write("\n")

print ""
print "Charl vs Dennis"
print "Increasing strength of both along columns. Increasing punching skill of both down rows."
print "All equally matched."
print "Entries have the form [win rate] ([mean number of rounds])."
for punching_train in range(4):
  for strength_train in range(4):
    C=Character("Charl")
    D=Character("Dennis")
    for i in range(punching_train):
      C.tree.descendant("punching").train()
      D.tree.descendant("punching").train()
    for i in range(strength_train):
      C.tree.descendant("strength").train()
      D.tree.descendant("strength").train()
    rounds, winrate = battle_data(C,D)
    sys.stdout.write(str(int(round(100*winrate)))+" ("+str(int(rounds))+")\t\t")
  sys.stdout.write("\n")

print ""
print "Charl vs Blobman"
print "Increasing strength of Charl along columns. Increasing punching skill of Charl down rows."
print "Top left is equally matched."
print "Entries have the form [win rate] ([mean number of rounds])."
for punching_train in range(4):
  for strength_train in range(4):
    C=Character("Charl")
    B=Character("Blobman", wound_zones_blob)
    for i in range(punching_train):
      C.tree.descendant("punching").train()
    for i in range(strength_train):
      C.tree.descendant("strength").train()
    rounds, winrate = battle_data(C,B)
    sys.stdout.write(str(int(round(100*winrate)))+" ("+str(int(rounds))+")\t\t")
  sys.stdout.write("\n")
