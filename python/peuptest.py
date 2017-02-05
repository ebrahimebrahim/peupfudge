#!/usr/bin/env python

# Peuptest, a testing framework for Peupfudge.

from monte_carlo import *
import os

list_of_trees_to_test = ["example.tree"]

def main():
  for t in list_of_trees_to_test:
    run_test(import_ability_tree(os.path.join("./trees/",t)))





if __name__=="__main__":
  main()
