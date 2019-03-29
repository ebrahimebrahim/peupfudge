import ability_tree as at
import monte_carlo as mc
import copy
import numpy as np

T=at.import_ability_tree("trees/example.tree")
T_initial = copy.deepcopy(T)
train_seq = []

while True:
    print("\n----------------------\n")
    print(T)
    print('')
    print("Which skill would you like to train?")
    while True:
        skill_name=raw_input()
        if skill_name == "done": break
        try:
            skill_to_train = T.descendant(skill_name)
            assert(skill_to_train.is_skill())
            break
        except:
            print("Try again, which skill would you like to train? Type the name of the skill and make sure it's a skill and not an attribute. Type \"done\" when done.")
    if skill_name == "done": break
    train_seq.append(skill_name)
    print('')
    skill_to_train.train(verbose=True)
    
N=1000
def trainer(tree):
    total_xp_cost = 0
    for skill_name in train_seq:
        total_xp_cost += tree.descendant(skill_name).train()
    return total_xp_cost
print("\n\n========\n")
print("Your training sequence was: "+str(train_seq)+'\n')
print("Running your training strategy {} times to gather statistics...\n".format(N))
outcomes,xp_costs = mc.run_trials(T_initial,trainer,num_trials=N,include_xpcosts=True)
mean_xp_cost = np.mean(xp_costs)
print("Average xp cost of your training strategy: {}\n".format(mean_xp_cost))
print(mc.percentiles_tree(T_initial, outcomes))
print('')
