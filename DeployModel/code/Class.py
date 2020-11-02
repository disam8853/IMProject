import random
import copy
import math
import numpy as np
import sys
import pandas as pd
from itertools import combinations 
inf = 99999999
big = 100000   # 必須 > (num_s + num_o + num_p + num_q)個數

class Node():
    def __init__(self, id, type, capacity_idx):
        self.id = id
        self.type = type
        self.capacity_idx = capacity_idx
        self.capacity, self.cost, self.capacity_list, self.cost_list = self.assign_attribute(self.type, self.capacity_idx)
    
    def __str__(self):
        return "{}{} with capacity index {}".format(self.type, self.id, self.capacity_idx)

    def assign_attribute(self, type, capacity_idx):
        # required : 1 - 5 (10 unit)
        capacity_df = pd.read_csv("./capacity.csv")
        if type == 'r':
            capacity_list = np.array(capacity_df['r']) # 單位：千元
            cost_list = capacity_list * 3 # (單位: unit), cost = capacity * 30
            capacity_list = list(capacity_list)
            cost_list = list(cost_list)
            capacity = capacity_list[capacity_idx]
            cost = cost_list[capacity_idx]
            return capacity, cost, capacity_list, cost_list

        elif type == 'o':
            capacity_list = np.array(capacity_df['r'])
            cost_list = capacity_list * 3
            capacity_list = list(capacity_list)
            cost_list = list(cost_list)
            capacity = capacity_list[capacity_idx]
            cost = cost_list[capacity_idx]
            return capacity, cost, capacity_list, cost_list
        
        elif type == 'p':
            capacity_list = np.array(capacity_df['r'])
            cost_list = capacity_list * 3
            capacity_list = list(capacity_list)
            cost_list = list(cost_list)
            capacity = capacity_list[capacity_idx]
            cost = cost_list[capacity_idx]
            return capacity, cost, capacity_list, cost_list

        elif type == 'q':
            capacity_list = np.array(capacity_df['r'])
            cost_list = capacity_list * 3
            capacity_list = list(capacity_list)
            cost_list = list(cost_list)
            capacity = capacity_list[capacity_idx]
            cost = cost_list[capacity_idx]
            return capacity, cost, capacity_list, cost_list
        
        elif type == 's':
            capacity_list = np.array(capacity_df['r'])
            cost_list = capacity_list * 3
            capacity_list = list(capacity_list)
            cost_list = list(cost_list)
            capacity = capacity_list[capacity_idx]
            cost = cost_list[capacity_idx]
            return capacity, cost, capacity_list, cost_list
        
        else:
            print('No such type.')
            return None, None, None 

class NodeSet():
    def __init__(self):
        self.nodes = []

    def __str__(self):
        string = ""
        for node in self.nodes:
            string += str(node) + '\n'
        return string
    
    def get_id(self):
        return len(self.nodes)
    
    def get_node(self, id):
        return self.nodes[id]
    
    def add_node(self, new_node):
        self.nodes.append(new_node)
    
    def length(self):
        return len(self.nodes)

# directed link
class Link():
    def __init__(self, id, type, node1, node2, capacity_idx):
        self.id = id
        self.type = type
        self.capacity_idx = capacity_idx
        #self.r_capacity_number = random.randint(3, 5)
        #self.o_capacity_number = random.randint(3, 5)
        #self.p_capacity_number = random.randint(3, 5)
        #self.q_capacity_number = random.randint(3, 5)
        #self.s_capacity_number = random.randint(3, 5)
        self.node1 = node1
        self.node2 = node2
        self.capacity, self.cost, self.capacity_list, self.cost_list = self.generate_capacity_cost(self.type, self.capacity_idx, self.node1)
    
    def __str__(self):
        if self.type == 'arti':
            return "artificial link {}: {}{} - {}{}".format(self.id, self.node1.type, self.node1.id, self.node2.type, self.node2.id)
        elif self.type == 'comm':
            return "communication link {}: {}{} - {}{}".format(self.id, self.node1.node1.type, self.node1.id, self.node2.node2.type, self.node2.id)
        else:
            return "Wrong link type."
    
    def generate_capacity_cost(self, type, capacity_idx, node):
        df = pd.read_csv("./comm.csv")
        if type == 'comm':
            capacity_list = np.array(df['capacity'])
            cost_list = capacity_list * 3
            capacity_list = list(capacity_list)
            cost_list = list(cost_list)
            capacity = capacity_list[capacity_idx]
            cost = cost_list[capacity_idx]
            return capacity, cost, capacity_list, cost_list

        elif type == 'arti':  # capacity 就是 node 的 capacity
            capacity = node.capacity
            cost = node.cost
            capacity_list = node.capacity_list
            cost_list = node.cost_list
            return capacity, cost, capacity_list, cost_list
        else:
            print('No such type.')
            return None, None
    
    def is_same(self, link):
        if link is None:
            print('link not exist')
            return False
        elif self.node1 == link.node1 and self.node2 == link.node2:
            return True
        else:
            return False
    
    def has_node(self, node):
        if self.node1 == node:  # 因為是directed link
            return True
        else:
            return False
    
class LinkSet():
    def __init__(self):
        self.links = []
    
    def __str__(self):
        string = ""
        for link in self.links:
            string += str(link) + "\n"
        return string
    
    def add_link(self, new_link):
        for link in self.links:
            if link.is_same(new_link):
                return 
        self.links.append(new_link)

    # def find_link(self, link):
    #     for item in self.links:
    #         if item.is_same(link):
    #             return item
    #     return None
    
    def find_link(self, link):
        if link in self.links:
            return self.links.index(link)
        else:
            # print("Link not exist.")
            return -1
    
    def get_link_by_node(self, node1, node2):
        for link in self.links:
            if link.node1.id == node1.id and link.node2.id == node2.id:
                return link
    
    def get_link(self, id):
        return self.links[id]
    
    def get_id(self):
        return len(self.links)
    
    def length(self):
        return len(self.links)
            
class Path():
    def __init__(self, id = 0, node_list = [], link_list = []):
        self.id = id
        self.node_list = node_list
        self.link_list = link_list
        self.cost = 0

    def __str__(self):
        string = "Path {}: ".format(self.id)
        for i in range(len(self.node_list)):
            if i == 0:
                string += "{}{}".format(self.node_list[i].node1.type, self.node_list[i].id)
            else:
                string += "-> {}{}".format(self.node_list[i].node1.type, self.node_list[i].id)
        return string
    
    def add_node(self, node):
        self.node_list.append(node)
    
    def add_link(self, link):
        self.link_list.append(link)
        # 哪些 path 不應該產生，就先濾掉
        # links 有順序性
    
    def get_path_cost(self, matrix):
        total = 0
        for link in self.link_list:
            node1_id, node2_id = link.node1.id, link.node2.id
            total += matrix[node1_id][node2_id]
        self.cost = total

class PathSet():
    def __init__(self, start: Link, end: Link):
        self.start = start
        self.end = end
        self.paths = []
    
    def __str__(self):
        string = "{}{}  -> {}{}: \n".format(self.start.node1.type, self.start.node1.id, self.end.node1.type, self.end.node1.id)
        for path in self.paths:
            string += str(path) + "\n"
        return string
    
    def add_path(self, path: Path):
        if path.node_list[0] == self.start and path.node_list[-1] == self.end:
            self.paths.append(path)
        else:
            print("Path doesn't match.")
            if path.node_list[0] != self.start and path.node_list[-1] == self.end:
                print("start node doesn't match.")
            elif path.node_list[0] == self.start and path.node_list[-1] != self.end:
                print("end node doesn't match.")
            else:
                print("start node and end node doesn't match.")
            return 
    
    def del_path(self, id):
        self.paths.remove(self.paths[id])

    def get_path(self, id):
        return self.paths[id]

    def length(self):
        return len(self.paths)

class Adjacency():
    def __init__(self):
        self.dic = dict()
        self.weighted_matrix = None
        self.matrix = None
        #self.init_weight = None
    
    def __str__(self):
        string = '=== Adjacency List ==='
        string += '\n'

        for key in self.dic:
            string += '{}{}: '.format(key.node1.type, key.id)
            for node in self.dic[key]:
                string += '-> {}{}'.format(node.node1.type, node.id)
            string += '\n'
        return string
    
    def get_matrix(self):
        node_num = len(self.dic.keys())
        matrix = np.zeros((node_num, node_num), dtype=int)
        for node in self.dic.keys():
            out_nodes = self.dic[node]
            in_id = node.id
            for out_node in out_nodes:   # assign link cost (for finding paths)
                out_id = out_node.id
                matrix[in_id][out_id] = 1
        return matrix
    
    def get_same_matrix(self):
        node_num = len(self.dic.keys())
        matrix = np.zeros((node_num, node_num), dtype=int)
        for i in range(node_num):
            for j in range(node_num):
                if i != j:
                    matrix[i][j] = inf

        for node in self.dic.keys():
            out_nodes = self.dic[node]
            in_id = node.id
            for out_node in out_nodes:   # assign link cost (for finding paths)
                out_id = out_node.id
                if node.node1.type == 'r' and out_node.node1.type == 'r':  # r_r 避免路徑會直接從r到r，r_r link間的cost要很大
                    matrix[in_id][out_id] = big
                elif node.node1.type in ['o', 'q', 'p'] and out_node.node1.type in ['o', 'q', 'p']:  
                    matrix[in_id][out_id] = 1
                elif node.node1.type in ['r', 's', 'o', 'p'] and out_node.node1.type in ['r', 's', 'o', 'p']:  # r_s, s_r, s_o, and p_s links
                    matrix[in_id][out_id] = 2
        return matrix
    
    def get_weighted_matrix(self):
        node_num = len(self.dic.keys())
        matrix = np.zeros((node_num, node_num), dtype=int)
        #self.init_weight = np.zeros((comm_links.length()))
        for i in range(node_num):
            for j in range(node_num):
                if i != j:
                    matrix[i][j] = inf

        for node in self.dic.keys():
            out_nodes = self.dic[node]
            in_id = node.id
            for out_node in out_nodes:   # assign link cost (for finding paths)
                out_id = out_node.id
                #link_id = comm_links.get_link_by_node(node, out_node).id
                if node.node1.type == 'r' and out_node.node1.type == 'r':  # r_r 避免路徑會直接從r到r，r_r link間的cost要很大
                    matrix[in_id][out_id] = big
                    #self.init_weight[link_id] = big
                elif node.node1.type in ['o', 'q', 'p'] and out_node.node1.type in ['o', 'q', 'p']:  
                    matrix[in_id][out_id] = 1
                    #self.init_weight[link_id] = big
                elif node.node1.type in ['r', 's', 'o', 'p'] and out_node.node1.type in ['r', 's', 'o', 'p']:  # r_s, s_r, s_o, and p_s links
                    matrix[in_id][out_id] = random.randint(1, 5)
        return matrix
    
    def get_lr_weighted_matrix(self, mu12, comm_links: LinkSet):
        node_num = len(self.dic.keys())
        matrix = np.zeros((node_num, node_num), dtype=int)
        for i in range(node_num):
            for j in range(node_num):
                if i != j:
                    matrix[i][j] = inf

        for node in self.dic.keys():
            out_nodes = self.dic[node]
            in_id = node.id
            for out_node in out_nodes:   # assign link cost (for finding paths)
                out_id = out_node.id
                link_id = comm_links.get_link_by_node(node, out_node).id
                if node.node1.type == 'r' and out_node.node1.type == 'r':  # r_r 避免路徑會直接從r到r，r_r link間的cost要很大
                    matrix[in_id][out_id] = big
                elif (node.node1.type == "o" and out_node.node1.type == "q") or (node.node1.type == "q" and out_node.node1.type == "p"):  # o_q, q_p
                    matrix[in_id][out_id] = 1
                elif (node.node1.type == "r" and out_node.node1.type == "s") or (node.node1.type == "s" and out_node.node1.type == "r") or (node.node1.type == "s" and out_node.node1.type == "o") or (node.node1.type == "p" and out_node.node1.type == "s"):
                    # matrix[in_id][out_id] = mu12[link_id]  # 若 initial mu12 >1 
                    matrix[in_id][out_id] = mu12[link_id]*10 + 1

        return matrix
        
    def add(self, node1, node2):
        self.dic.setdefault(node1, []).append(node2)
    
    def get(self, key):
        if key not in self.dic.keys():
            print('No such node.')
            return 
        else:
            return self.dic[key]
                    
# 目前是指定 userpair 的 origin 跟 destination 於兩個不同的 SDN router  
class UserPair():
    def __init__(self, id, r_loc: LinkSet, adjacency: Adjacency, comm_links: LinkSet, arti_nodes: LinkSet, s_loc_num: int):
        self.id = id
        self.r_loc = r_loc
        self.adjacency = adjacency
        self.weighted_matrix = self.adjacency.get_weighted_matrix()
        self.lr_weighted_matrix = None
        self.comm_links = comm_links
        self.arti_nodes = arti_nodes
        self.origin, self.destination = self.generate_origin_des()
        self.traffic = random.randint(10, 60)    # 單位: unit 
        self.path_number = random.randint(2, s_loc_num//2)
        self.selected_o = LinkSet()
        self.path_set = self.generate_paths('dijk') 
        
    def __str__(self):
        return "User pair{}: ({}{},{}{})".format(self.id, self.origin.node1.type, self.origin.node1.id, self.destination.node1.type, self.destination.node1.id)

    def generate_origin_des(self):   # Return origin, destination (artificial link). 
        data = [i for i in range(self.r_loc.length())]
        res = random.sample(data, 2)
        origin, destination =  self.r_loc.get_link(res[0]), self.r_loc.get_link(res[1])
        return origin, destination
    
    def generate_paths(self, method: str):  # 使用 k link(node) disjoint shortest paths 找路徑

        # Determine the shortest path from origin to des
        if method == 'dijk':
            A = PathSet(self.origin, self.destination); B = PathSet(self.origin, self.destination)   # 裝paths
            matrix = copy.deepcopy(self.weighted_matrix)
            path, matrix = self.Dijkstra(self.origin, self.destination, matrix)
            # 移除用過的 r_s link 
            matrix[path.link_list[0].node1.id][path.link_list[0].node2.id] = inf
            # 移除用過的 s_r link  
            matrix[path.link_list[-1].node1.id][path.link_list[-1].node2.id] = inf
            A.add_path(path)

            for k in range(1, self.path_number):
                for i in range(len(A.get_path(k-1).node_list)-1):
                    remove_links = []
                    spurNode = A.get_path(k-1).node_list[i]
                    if spurNode.node1.type in ['o', 'q', 'p', 's']:
                        continue            
                    # sequence of nodes from the source to the spur node of the previous k-shortest path
                    rootPath = Path()
                    rootPath.node_list = A.get_path(k-1).node_list[:i+1]
                    rootPath.link_list = A.get_path(k-1).link_list[:i]
                    for path in A.paths:  # Remove links from graph
                        if rootPath.node_list == path.node_list[:i+1] and rootPath.link_list == path.link_list[:i] and A.length() > 1:
                            # Remove the links that are part of the previous shortest paths which share the same root
                            remove_link = path.link_list[i]
                            if remove_link: 
                                remove_links.append(remove_link)
                                matrix[remove_link.node1.id][remove_link.node2.id] = inf

                    if len(rootPath.node_list) > 1:
                        for node in rootPath.node_list[:-1]:  # Remove nodes from graph
                            # remove node from graph
                            for i in range(len(matrix)):
                                if i != node.id:
                                    matrix[node.id][i] = inf
                                    matrix[i][node.id] = inf
                    
                    # Find spur path from the apur node to the sink(destination)
                    spurPath, matrix = self.Dijkstra(spurNode, self.destination, matrix)
                    
                    totalPath = Path(id=k)
                    totalPath.node_list = rootPath.node_list[:-1] + spurPath.node_list
                    totalPath.link_list = rootPath.link_list + spurPath.link_list

                    if totalPath not in B.paths:
                        B.add_path(totalPath)

                    # Add back the edges and nodes that were removed from the graph.
                    # Add back links
                    for link in remove_links:
                        matrix[link.node1.id][link.node2.id] = self.weighted_matrix[link.node1.id][link.node2.id]

                    # Add back nodes
                    for node in rootPath.node_list[:-1]:  # Remove nodes from graph
                        # remove node from graph
                        for i in range(len(matrix)):
                            matrix[node.id][i] = self.weighted_matrix[node.id][i]
                            if self.arti_nodes.get_link(i) in self.selected_o.links:
                                matrix[node.id][i] = inf

                if B.length() == 0:
                    break
                    
                A.add_path(B.get_path(0))
                # 移除用過的r_s link
                matrix[B.get_path(0).link_list[0].node1.id][B.get_path(0).link_list[0].node2.id] = inf
                matrix[B.get_path(0).link_list[-1].node1.id][B.get_path(0).link_list[-1].node2.id] = inf
                B.del_path(0)
            self.selected_o.links = []
            return A
        elif method == "lr":
            A = PathSet(self.origin, self.destination); B = PathSet(self.origin, self.destination)   # 裝paths
            matrix = copy.deepcopy(self.lr_weighted_matrix)

            path, matrix = self.lr_Dijkstra(self.origin, self.destination, matrix)
            # 移除用過的r_s link
            matrix[path.link_list[0].node1.id][path.link_list[0].node2.id] = inf
            matrix[path.link_list[-1].node1.id][path.link_list[-1].node2.id] = inf
            A.add_path(path)
            # for link in path.link_list:
            #     print(link)

            for k in range(1, self.path_number):
                for i in range(len(A.get_path(k-1).node_list)-1):
                    remove_links = []
                    spurNode = A.get_path(k-1).node_list[i]
                    if spurNode.node1.type in ['o', 'q', 'p', 's']:   # add 's'
                        continue
                    #print("spurNode: {}{}".format(spurNode.node1.type, spurNode.id))
            
                    # sequence of nodes from the source to the spur node of the previous k-shortest path
                    rootPath = Path()
                    rootPath.node_list = A.get_path(k-1).node_list[:i+1]
                    rootPath.link_list = A.get_path(k-1).link_list[:i]
                    #print("rootPath: {}".format(str(rootPath)))
                    for path in A.paths:  # Remove links from graph
                        if rootPath.node_list == path.node_list[:i+1] and rootPath.link_list == path.link_list[:i] and A.length() >= 1:   # > 1
                            # Remove the links that are part of the previous shortest paths which share the same root
                            remove_link = path.link_list[i]
                            if remove_link:   # ------------------------   link(i, i+1)會是不存在的link ???? -------------------------------------------
                                remove_links.append(remove_link)
                                matrix[remove_link.node1.id][remove_link.node2.id] = inf

                    if len(rootPath.node_list) > 1:
                        for node in rootPath.node_list[:-1]:  # Remove nodes from graph
                            # remove node from graph
                            for i in range(len(matrix)):
                                if i != node.id:
                                    matrix[node.id][i] = inf
                                    matrix[i][node.id] = inf
                    
                    # Find spur path from the apur node to the sink(destination)
                    spurPath, matrix = self.lr_Dijkstra(spurNode, self.destination, matrix)
                    
                    totalPath = Path(id=k)
                    totalPath.node_list = rootPath.node_list[:-1] + spurPath.node_list
                    totalPath.link_list = rootPath.link_list + spurPath.link_list

                    if totalPath not in B.paths:
                        B.add_path(totalPath)

                    # Add back the edges and nodes that were removed from the graph.
                    # Add back links
                    for link in remove_links:
                        matrix[link.node1.id][link.node2.id] = self.lr_weighted_matrix[link.node1.id][link.node2.id]

                    # Add back nodes
                    for node in rootPath.node_list[:-1]:  # Remove nodes from graph
                        # remove node from graph
                        for i in range(len(matrix)):
                            matrix[node.id][i] = self.lr_weighted_matrix[node.id][i]
                            if self.arti_nodes.get_link(i) in self.selected_o.links:
                                matrix[node.id][i] = inf

                if B.length() == 0:
                    break
                    
                A.add_path(B.get_path(0))
                # 移除用過的r_s link
                matrix[B.get_path(0).link_list[0].node1.id][B.get_path(0).link_list[0].node2.id] = inf
                matrix[B.get_path(0).link_list[-1].node1.id][B.get_path(0).link_list[-1].node2.id] = inf
                B.del_path(0)
            self.selected_o.links = []
            return A

    def generate_paths_s(self, method: str):
        if method == "dijk":
            container = PathSet(self.origin, self.destination)
            matrix = copy.deepcopy(self.weighted_matrix)
            path1, matrix = self.Dijkstra(self.origin, self.destination, matrix)

            matrix[path1.link_list[0].node1.id][path1.link_list[0].node2.id] = inf
            matrix[path1.link_list[-1].node1.id][path1.link_list[-1].node2.id] = inf
            container.add_path(path1)

            # Remove links directed into origin and reverse the direction of the zero length edges along path1
            matrix_res = copy.deepcopy(matrix)
            for i in range(len(path1.node_list)-1):
                out_node_id = path1.node_list[i+1].id
                matrix_res[out_node_id][path1.node_list[i].id] = matrix_res[path1.node_list[i].id][out_node_id]
                matrix_res[path1.node_list[i].id][out_node_id] = inf
            
            for node in path1.node_list:
                if node.node1.type in ['o', 'q', 'p', 's']:
                    array_1 = np.zeros(len(matrix))
                    array_1.fill(inf)
                    array_1[node.id] = 0
                    matrix[:, node.id] = array_1
            path2, matrix = self.Dijkstra(self.origin, self.destination, matrix)
            container.add_path(path2)
            return container
        elif method == "lr":
            container = PathSet(self.origin, self.destination)
            matrix = copy.deepcopy(self.weighted_matrix)
            path1, matrix = self.Dijkstra(self.origin, self.destination, matrix)

            matrix[path1.link_list[0].node1.id][path1.link_list[0].node2.id] = inf
            matrix[path1.link_list[-1].node1.id][path1.link_list[-1].node2.id] = inf
            container.add_path(path1)

            # Remove links directed into origin and reverse the direction of the zero length edges along path1
            matrix_res = copy.deepcopy(matrix)
            for i in range(len(path1.node_list)-1):
                out_node_id = path1.node_list[i+1].id
                matrix_res[out_node_id][path1.node_list[i].id] = matrix_res[path1.node_list[i].id][out_node_id]
                matrix_res[path1.node_list[i].id][out_node_id] = inf
            
            for node in path1.node_list:
                if node.node1.type in ['o', 'q', 'p', 's']:
                    array_1 = np.zeros(len(matrix))
                    array_1.fill(inf)
                    array_1[node.id] = 0
                    matrix[:, node.id] = array_1
            path2, matrix = self.Dijkstra(self.origin, self.destination, matrix)
            container.add_path(path2)
            return container

    def Dijkstra(self, start: Link, end: Link, matrix):
        start_id = start.id
        end_id = end.id
        dis = np.zeros(len(matrix), dtype=int)
        paths = [] # 存放 start 到 node(i)的路徑節點集合
        for i in range(len(matrix)):
            dis[i] = matrix[start_id][i]
            paths.append(Path(id=i, node_list=[start])) 
        
        # Initialize used array
        used = np.zeros(len(matrix), dtype=int)
        used[start_id] = 1
        #print("dis: {}".format(dis))

        for i in range(len(matrix)-1):
            # 找離start最近的點
            min = inf
            u = 0
            for j in range(len(matrix)):
                if used[j] == 0 and dis[j] < min:
                    min = dis[j]
                    u = j
            used[u] = 1
            #print("find node {}".format(u))
            for v in range(len(matrix)):
                if matrix[u][v] < inf:  # u,v 之間有 link
                    if dis[v] > dis[u] + matrix[u][v]:
                        dis[v] = dis[u] + matrix[u][v]
                        paths[v].node_list = paths[u].node_list + [self.arti_nodes.get_link(u)]
                        paths[v].link_list = paths[u].link_list + [self.comm_links.get_link_by_node(paths[u].node_list[-1], self.arti_nodes.get_link(u))]
                        # if v == end_id:
                        #     print(self.arti_nodes.get_link(u))
                        #     print(self.comm_links.get_link_by_node(paths[u].node_list[-1], self.arti_nodes.get_link(u)))
        # 將每個path加入dis[i]的node i(end_node)
        # 只加要找的那個path就好
        paths[end_id].add_node(self.arti_nodes.get_link(end_id))
        link = self.comm_links.get_link_by_node(paths[end_id].node_list[-2], self.arti_nodes.get_link(end_id))
        if link is not None:
            #print("{}{}-{}{} is None".format(paths[end_id].node_list[-2].node1.type, paths[end_id].node_list[-2].id, self.arti_nodes.get_link(end_id).node1.type, self.arti_nodes.get_link(end_id).id))
            paths[end_id].add_link(link)
        # else:
        #     print(str(paths[end_id].node_list[-1])+"->"+str(self.arti_nodes.get_link(end_id))+" not exist.")

        #paths[end_id].add_link(self.comm_links.get_link_by_node(paths[end_id].node_list[-2], self.arti_nodes.get_link(end_id))) 

        # 將所有連到所選到的o node的cost設很大，防止其他k-1條path再選到這條o-q-p組合
        for node in paths[end_id].node_list:
            if node.node1.type == 'o':
                self.selected_o.add_link(node)
                array_1 = np.zeros(len(matrix))
                array_1.fill(inf)
                array_1[node.id] = 0
                matrix[:, node.id] = array_1
                break
        return paths[end_id], matrix
    
    def lr_Dijkstra(self, start: Link, end: Link, matrix):
        start_id = start.id
        end_id = end.id
        dis = np.zeros(len(matrix), dtype=int)
        paths = [] # 存放 start 到 node(i)的路徑節點集合
        for i in range(len(matrix)):
            dis[i] = matrix[start_id][i]
            paths.append(Path(id=i, node_list=[start], link_list=[])) 
        
        # Initialize used array
        used = np.zeros(len(matrix), dtype=int)
        used[start_id] = 1

        for i in range(len(matrix)-1):
            # 找離start最近的點
            min = inf
            u = 0
            for j in range(len(matrix)):
                if used[j] == 0 and dis[j] < min:
                    min = dis[j]
                    u = j
            used[u] = 1
            for v in range(len(matrix)):
                if matrix[u][v] < inf:  # u,v 之間有 link
                    if dis[v] > dis[u] + matrix[u][v]:
                        dis[v] = dis[u] + matrix[u][v]
                        paths[v].node_list = paths[u].node_list + [self.arti_nodes.get_link(u)]
                        paths[v].link_list = paths[u].link_list + [self.comm_links.get_link_by_node(paths[v].node_list[-2], paths[v].node_list[-1])]

        # 將每個path加入dis[i]的node i(end_node)
        # 只加要找的那個path就好
        if paths[end_id].node_list[-1] != self.arti_nodes.get_link(end_id):
            paths[end_id].add_node(self.arti_nodes.get_link(end_id))
            link = self.comm_links.get_link_by_node(paths[end_id].node_list[-2], paths[end_id].node_list[-1])
            if link is not None:
                paths[end_id].add_link(link)

        # 將所有連到所選到的o node的cost設很大，防止其他k-1條path再選到這條o-q-p組合
        for node in paths[end_id].node_list:
            if node.node1.type == 'o':
                self.selected_o.add_link(node)
                array_1 = np.zeros(len(matrix))
                array_1.fill(inf)
                array_1[node.id] = 0
                matrix[:, node.id] = array_1
                break
        return paths[end_id], matrix
           
class UserpairSet():
    def __init__(self):
        self.pairs = []

    def __str__(self):
        string = ""
        for i in range(len(self.pairs)):
            string += "pair {}: {}{} -> {}{}".format(self.pairs[i].id, self.pairs[i].origin.node1.type, 
            self.pairs[i].origin.node1.id, self.pairs[i].destination.node1.type, self.pairs[i].destination.node1.id)
            string += "\n"
        return string
    
    def get_pair(self, id):
        return self.pairs[id]
    
    def add_pair(self, pair):
        if pair not in self.pairs:
            self.pairs.append(pair)
            #print("Add pair {}".format(pair.id))
        else:
            print('This pair is already exists.')
    
    def length(self):
        return len(self.pairs)

    def get_all_traffic(self):
        traffic = 0
        for pair in self.pairs:
            traffic += pair.path_number * pair.traffic
        return traffic

    
    



if __name__ == '__main__':
    node1 = Node(1, 'q', 2)
    node2 = Node(2, 's', 2)
    node3 = Node(3, 'p', 1)
    link1 = Link(1, 'arti', node1, node1, 3)
    link2 = Link(2, 'arti', node2, node2, 3)
    link3 = Link(3, 'comm', link1, link2, 2)
    link4 = Link(4, 'comm', link1, link2, 1)
    print(link3.is_same(link4))
    # print(link4.has_node(link1))
    print(link2)
    print(link4)
