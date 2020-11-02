from link import generate_links_from_file, generate_complete_graph, auto_generate_sparse_graph
from lr import LR
from config import NODES, NODES_COUNT, ITER_LIMIT, IMPROVE_LIMIT, LB, GAP_MINIMUM, lamda, priorityNum, LINKS_COUNT
from odpair import Path, ODpair
from primal import Primal
from random import sample
import math
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import random        
import pickle
import sys


linkset = []
node_set = NODES


link_set = auto_generate_sparse_graph(node_set, LINKS_COUNT-NODES_COUNT+1)
pickle.dump(link_set,open("linkset.pkl","wb"))


#link_set = pickle.load(open("linkset.pkl","rb"))

print("=== Links Set ===")
print(link_set)

odpair_set = []
prioritylv = priorityNum



print("=== O-D pairs probably paths ===")

for i in range(len(NODES)):
    src = NODES[i]
    dst = NODES.copy()
    dst.remove(src)
    for dst_node in dst:
        odpair = ODpair(src,dst_node)
        odpair.generate_path(link_set)
        odpair_set.append(odpair)
        print(odpair)

pickle.dump(odpair_set,open("odpair_set.pkl","wb"))  


#odpair_set = pickle.load(open("odpair_set.pkl","rb"))    


improve_counter = 0
C = 20
UBList = []
LBList = []
z_starList = []

primal = Primal(odpair_set,link_set,prioritylv)
lr = LR(odpair_set,link_set,prioritylv)


primal.initialize_decision_variables()
z_star,initial_d = primal.initial_solution()
#z_star = math.inf
initial_value = z_star
print("initial solution value:", z_star)


mu = lr.initialize_lr_multiplier()

# 避免LR方法每回合皆設定相同k,以每回合給定k的比例重新分配a_wlk
k_count = [0] * prioritylv
def awlk_count(lr_a_wlk):
    count = [0] * prioritylv
    for w in range(len(odpair_set)):
        for l in range(link_set.length()):
            for k in range(prioritylv):
                if(lr_a_wlk[w][l][k] == 1):
                    count[k] += 1
    return count.index(max(count))

def awlk_prob(k_count,lr_a_wlk):
    rand_k = [k for k in range(prioritylv)]
    prob_k = [0] * prioritylv
    total = sum(k_count)
    for k in range(prioritylv):
        prob_k[k] = k_count[k]/total
    arr_prob_k = np.array(prob_k)
    for w in range(len(odpair_set)):
        for l in range(link_set.length()):
            lr_a_wlk[w][l] = sys.float_info.epsilon
            index = np.random.choice(rand_k, p = arr_prob_k)
            lr_a_wlk[w][l][index] = 1.0   
    return lr_a_wlk

for i in range(ITER_LIMIT):
    lr.initialize_decision_variables()
    zd  = lr.sol_sub1() + lr.sol_sub2() + lr.sol_sub3() + lr.sol_sub4() + lr.sol_sub5() + lr.sol_sub6_1() + lr.sol_sub6_2() + lr.sol_sub7() + lr.sol_sub8() + lr.sol_sub9() + lr.sol_sub10() + lr.sol_sub11() + lr.sol_sub12()     
    improve_counter = improve_counter + 1 if zd < LB else 0
    LB = max(LB, zd)
    LBList.append(LB)
    print(LB,zd)
    
    lr_a_wlk = lr.a_vaule()
    k_count[awlk_count(lr_a_wlk)] += 1
    lr_a_wlk = awlk_prob(k_count,lr_a_wlk)

    #UB = math.inf

    UB = primal.get_primal_feasible(mu,lr_a_wlk)
    
    x_wp = lr.x_value()
    z_starList.append(z_star)
    z_star = min(z_star, UB)
    
    

    print("{}: UB={} Z*={} LB={}".format(i+1, UB, z_star, LB))
    print( "GAP", abs(z_star-LB) / min( abs(z_star) , abs(LB)))
    
    if LB > z_star:
        print("LB > z_star!!!")
        print("Stop at iteration {}".format(i+1))
        break
    elif i+1 == ITER_LIMIT:
        print("iteration limit reached!")
        print("Stop at iteration {}".format(i+1))
        break
    
    
    elif ( abs(z_star-LB) / min( abs(z_star) , abs(LB) ) < GAP_MINIMUM):
        print("Gap minimum reached!")
        print("Stop at iteration {}".format(i+1))
        break
    
    
    if (improve_counter == IMPROVE_LIMIT):
        lamda /= 2
        improve_counter = 0
    
    
    lr.adjust_multiplier_denominator(lamda, z_star, zd)    
    #lr.adjust_multiplier(C, i+1) 


font = {'weight' : 'normal',
        'size'   : 12}
matplotlib.rc('font', **font)
figure, ax = plt.subplots(figsize = (8,4), dpi=100)
ax.plot(z_starList, label="Z*", color="darkseagreen", linewidth=2)
ax.plot(LBList, label="Lower Bound", color="cadetblue", linewidth=2)
ax.legend(loc="lower right")
ax.set_title("Z* and Lower Bound in Lagrangian Relaxation")
ax.set_xlabel("Iteration")
ax.set_ylabel("Objective Value")
figure.tight_layout()
plt.savefig("primal"+".png")
plt.show()


f = open("output.txt", "w")
f.write("Topology: \n")
for l in range(link_set.length()):
    f.write("link " + str(l) + " : node " + str(link_set.links[l].node1) + " - node " + str(link_set.links[l].node2) + " Service Rate: " + str(link_set.links[l].svcRate) + "\n")
f.write("\nO-D pair Results: \n")    
for w in range(len(odpair_set)):
    f.write("O-D pair "+str(w)+" "+str(odpair_set[w].start)+" -> "+str(odpair_set[w].end))
    for p in range(len(x_wp[w])):
        if(x_wp[w][p] == 1):
            f.write(": "+str(odpair_set[w].paths[p].node_list)+" Priority k = [")
            for l in range(len(odpair_set[w].paths[p].link_list)):
                for k in range(prioritylv):
                    if(lr_a_wlk[w][l][k] == 1):
                        f.write(str(k))
                        if(l!=len(odpair_set[w].paths[p].link_list)-1):
                            f.write(", ")
            f.write("] \n")
f.close()




    