#%%
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime

def JudgeStyle(data, node_style):
    if data < node_style[0]:
        return 'r'
    elif data >= node_style[0] and data < node_style[1]:
        return 'o'
    elif data >= node_style[1] and data < node_style[2]:
        return 'p'
    elif data >= node_style[2] and data < node_style[3]:
        return 'q'
    else:
        return 's'

# %%
def show_path(config_loc):
    f = open("output.txt", 'r')
    output = f.read()
    f.close()
    node = output.split("\n")[0]
    link = output.split("\n")[3]
    node_level = output.split("\n")[1]
    link_level = output.split("\n")[4]
    # %%
    def DataPre(style:str, line: str):
        line = line.replace(style+": [", "")
        line = line.replace("]", "")
        line = line.split(", ")
        line = np.array(line, dtype=int)
        return line
    node = DataPre("Node", node)
    link = DataPre("Link", link)
    node_level = DataPre("Capacity level", node_level)
    link_level = DataPre("Capacity level", link_level)

    # %%
    config = open(config_loc, "r")
    lines = config.readlines()

    for i, line in enumerate(lines):
        # print(line)
        if i == 0:
            USERPAIR_NUM = int(line)
        elif i == 1:
            traffic_list = [int(num) for num in line.split(',')]
        elif i == 2:
            pathnum_list = [int(num) for num in line.split(',')]
        elif i == 3:
            R_NUM = int(line)
        elif i == 4:
            O_NUM = int(line)
        elif i == 5:
            P_NUM = int(line)
        elif i == 6:
            Q_NUM = int(line)
        else:
            S_NUM = int(line)
    print(R_NUM, O_NUM, P_NUM, Q_NUM, S_NUM)

    node_num = [R_NUM, O_NUM, P_NUM, Q_NUM, S_NUM]
    node_style = []
    tmp = 0
    for i in node_num:
        tmp += i
        node_style.append(tmp)
    print(node_style)
    #%%

    df = pd.read_csv("./link.csv")

    capa = pd.read_csv("capacity.csv")
    #%%


    last = df['origin'][link[0]]
    count = 0
    ind = 0
    link_dict = {}
    key = "Method " + str(count)
    link_dict[key] = {}
    link_dict[key]["link"] = []
    link_dict[key]["capacity"] = []
    print("Method {}:".format(count))
    for idx in link:
        if last != df['origin'][idx]:
            
            link_dict[key]["link"].append(int(last))
            count += 1
            key = "Method " + str(count)
            link_dict[key] = {}
            link_dict[key]["link"] = []
            link_dict[key]["capacity"] = []
            print("{}\n\nMethod {}:".format(last,count))
        # print("{} -> {}".format(df["origin"][idx], df["destination"][idx]))
        style = JudgeStyle(idx, node_style)
        capacity = capa[style][link_level[ind]]
        
        link_dict[key]["link"].append(int(df["origin"][idx]))
        link_dict[key]["capacity"].append(int(capacity))
        print("{} =({})=> ".format(df["origin"][idx], capacity), end="")
        last = df["destination"][idx]
        ind += 1

    link_dict[key]["link"].append(int(last))
    print(last)

    print(link_dict)

    try:
        os.mkdir("./path")
    except:
        pass

    fname = "./path/result_"
    fname += (str(datetime.now().date()).replace("-", "") 
            + "_" 
            + str(datetime.now().time()).replace(":", "")[:6]
            + ".json")
    with open(fname, "w") as jsfile:
        json.dump(link_dict, jsfile)

    with open("./path/result.json", "w") as jsfile:
        json.dump(link_dict, jsfile)
if __name__ == "__main__":
    show_path("./my_config.txt")
# #%%
# print(ind)
# print(len(node))
# print(len(node_level))
