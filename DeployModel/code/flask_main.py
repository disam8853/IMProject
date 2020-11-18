
# %%
import random
import math
import numpy as np
from Class import *
from LR import LR
import time
import sys


# %%
# Create nodes (including in-nodes and out-nodes of 5 types of nodes)
def create_nodes(r_num: int, o_num: int, p_num: int, q_num: int, s_num: int):
    # The number of processor, observser, and LAN should be the same
    # cloud router 分成 in-set 跟 out-set，由 SDN network 進入 cloud 的 traffic 只能由 in_cloud_outer_set 傳到 observers; out_cloud_router_set
    # 負責把 processors 出來的 traffic 導回 SDN network
    r_in = NodeSet()
    r_out = NodeSet()
    o_in = NodeSet()
    o_out = NodeSet()
    p_in = NodeSet()
    p_out = NodeSet()
    q_in = NodeSet()
    q_out = NodeSet()
    s_in = NodeSet()
    s_out = NodeSet()
    idx = 0
    # id從r開始往上加
    for i in range(r_num):
        node = Node(idx, 'r', 1)
        r_in.add_node(node)
        r_out.add_node(node)
        idx += 1

    for i in range(o_num):
        node = Node(idx, 'o', 1)
        o_in.add_node(node)
        o_out.add_node(node)
        idx += 1

    for i in range(p_num):
        node = Node(idx, 'p', 1)
        p_in.add_node(node)
        p_out.add_node(node)
        idx += 1

    for i in range(q_num):
        node = Node(idx, 'q', 1)
        q_in.add_node(node)
        q_out.add_node(node)
        idx += 1

    for i in range(s_num):
        node = Node(idx, 's', 1)
        s_in.add_node(node)
        s_out.add_node(node)
        idx += 1

    return r_in, r_out, o_in, o_out, p_in, p_out, q_in, q_out, s_in, s_out
# Initiate the artificial link (representing a node after node-splitting) on corresponding location.
# Artificial link : node1 為一 in-node，node2 為一 out-node


def create_location_list(r_in: NodeSet, r_out: NodeSet, o_in: NodeSet, o_out: NodeSet, p_in: NodeSet,
                         p_out: NodeSet, q_in: NodeSet, q_out: NodeSet, s_in: NodeSet, s_out: NodeSet):
    r_loc = LinkSet()
    o_loc = LinkSet()
    p_loc = LinkSet()
    q_loc = LinkSet()
    s_loc = LinkSet()
    arti_nodes = LinkSet()

    for i in range(r_in.length()):
        node = Link(r_in.get_node(i).id, 'arti',
                    r_in.get_node(i), r_out.get_node(i), 1)
        r_loc.add_link(node)
        arti_nodes.add_link(node)

    for i in range(o_in.length()):
        node = Link(o_in.get_node(i).id, 'arti',
                    o_in.get_node(i), o_out.get_node(i), 1)
        o_loc.add_link(node)
        arti_nodes.add_link(node)

    for i in range(p_in.length()):
        node = Link(p_in.get_node(i).id, 'arti',
                    p_in.get_node(i), p_out.get_node(i), 1)
        p_loc.add_link(node)
        arti_nodes.add_link(node)

    for i in range(q_in.length()):
        node = Link(q_in.get_node(i).id, 'arti',
                    q_in.get_node(i), q_out.get_node(i), 1)
        q_loc.add_link(node)
        arti_nodes.add_link(node)

    for i in range(s_in.length()):
        node = Link(s_in.get_node(i).id, 'arti',
                    s_in.get_node(i), s_out.get_node(i), 1)
        s_loc.add_link(node)
        arti_nodes.add_link(node)

    return r_loc, o_loc, p_loc, q_loc, s_loc, arti_nodes

# Create given communication links


def generate_comm_link(r_loc: LinkSet, o_loc: LinkSet, p_loc: LinkSet, q_loc: LinkSet, s_loc: LinkSet):
    idx = r_loc.length() + o_loc.length() + p_loc.length() + \
        q_loc.length() + s_loc.length()
    comm_linkset = LinkSet()
    adjacency = Adjacency()
    # weights = [] # mu12 init value

    def add_comm(node1, node2, capacity_idx):
        comm_linkset.add_link(
            Link(comm_linkset.get_id(), 'comm', node1, node2, capacity_idx))
        adjacency.add(node1, node2)

    # r_r_link (bidirection)
    for idx, node1 in enumerate(r_loc.links):
        for node2 in r_loc.links[idx+1:]:
            capacity_idx = random.randint(1, 3)
            add_comm(node1, node2, capacity_idx)
            # weights.append(big)
            add_comm(node2, node1, capacity_idx)
            # weights.append(big)

    # r_s_link (single-direction)
    out_s_idx = (s_loc.length() // 2)
    for r_node in r_loc.links:
        for s_node in s_loc.links[:out_s_idx]:
            add_comm(r_node, s_node, random.randint(1, 3))

    # sIn_o_link (single-direction)
    for s_node in s_loc.links[:out_s_idx]:
        for o_node in o_loc.links:
            add_comm(s_node, o_node, random.randint(1, 3))

    # o_q_link (single-direction)
    for i in range(o_loc.length()):
        add_comm(o_loc.get_link(i), q_loc.get_link(i), random.randint(1, 3))

    # q_p_link (single-direction)
    for i in range(q_loc.length()):
        add_comm(q_loc.get_link(i), p_loc.get_link(i), random.randint(1, 3))

    # p_sOut_link (single-direction)
    for p_node in p_loc.links:
        for s_node in s_loc.links[out_s_idx:]:
            add_comm(p_node, s_node, random.randint(1, 3))

    # sOut_r_link (single-direction)
    for s_node in s_loc.links[out_s_idx:]:
        for r_node in r_loc.links:
            add_comm(s_node, r_node, random.randint(1, 3))

    return comm_linkset, adjacency

# %%


def run_deploy(iter_times=100, start_node=None, dest_node=None, config_loc="./config.txt"):

    inf = 99999999
    big = 1000
    # t_start = time.clock()
    random.seed(1)
    # Read config file
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

    RO = 0.9
    DELAY_TOLER = 3

    r_in, r_out, o_in, o_out, p_in, p_out, q_in, q_out, s_in, s_out = create_nodes(
        R_NUM, O_NUM, P_NUM, Q_NUM, S_NUM)
    r_loc, o_loc, p_loc, q_loc, s_loc, arti_nodes = create_location_list(
        r_in, r_out, o_in, o_out, p_in, p_out, q_in, q_out, s_in, s_out)
    comm_links, adjacency = generate_comm_link(
        r_loc, o_loc, p_loc, q_loc, s_loc)
    print("Number of links: ", comm_links.length())

    # %%
    link_present = []
    for i in comm_links.links:
        link_present.append([i.id, i.node1.id, i.node2.id])
    df = pd.DataFrame(np.array(link_present), columns=[
                      "id", "origin", "destination"])
    df.to_csv("link.csv", index=0)
    # print(adjacency.get_matrix())

    # %%
    print(r_loc.get_link(5).capacity_list)

    # %%
    df = pd.DataFrame(adjacency.get_matrix())
    df.to_csv("adjacency.csv", index=False)
    print(np.sum(adjacency.get_matrix()))

    # %%
    user_pairs = UserpairSet()
    for i in range(USERPAIR_NUM):
        pair = UserPair(i, r_loc, adjacency, comm_links,
                        arti_nodes, s_loc.length())
        pair.traffic = traffic_list[i]
        pair.path_number = pathnum_list[i]
        if start_node != None and dest_node != None:
            pair.origin = r_loc.get_link(start_node)
            pair.destination = r_loc.get_link(dest_node)
        else:
            pair.path_set = pair.generate_paths('dijk')
        # pair.path_set = pair.generate_paths('dijk') if pair.path_number > 2 else pair.generate_paths_s('dijk')
        user_pairs.add_pair(pair)

    # %%

    __LR = LR(r_loc, o_loc, p_loc, q_loc, s_loc, RO,
              DELAY_TOLER, comm_links, user_pairs)
    __LR.initialize_decision_variables()
    __LR.initialize_lr_multiplier()
    Z_star = __LR.initialize()
    print("Z_star", Z_star)
    iter_limit = iter_times

    result = __LR.lagrangian_relaxation(Z_star, 0, iter_limit)
    return result


if __name__ == "__main__":
    run_deploy(int(sys.argv[1]), int(sys.argv[2]),
               int(sys.argv[3]), sys.argv[4])
