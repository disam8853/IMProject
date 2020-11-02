#%%
import numpy as np
import pandas as pd
# %%
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
config = open("origin_config.txt", "r")
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
capa
#%%
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


last = df['origin'][link[0]]
count = 0
ind = 0
print("Method {}:".format(count))
for idx in link:
    if last != df['origin'][idx]:
        count += 1
        print("{}\n\nMethod {}:".format(last,count))
    # print("{} -> {}".format(df["origin"][idx], df["destination"][idx]))
    style = JudgeStyle(idx, node_style)
    capacity = capa[style][link_level[ind]]
    print("{} =({})=> ".format(df["origin"][idx], capacity), end="")
    last = df["destination"][idx]
    ind += 1

print(last)

#%%
print(ind)
print(len(node))
print(len(node_level))