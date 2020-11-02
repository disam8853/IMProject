import random
from config import maxDelayTol_lk, priorityNum, d_lk_gap, minSvcRate, maxSvcRate


class Link():
    def __init__(self, id, node1, node2):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.svcRate = random.randint(minSvcRate,maxSvcRate)
        DelayTol_lk = [maxDelayTol_lk] * priorityNum
        for k in range(len(DelayTol_lk)):
            DelayTol_lk[k] = maxDelayTol_lk - (k*d_lk_gap)
        self.delayTol = DelayTol_lk
        
        
    def __str__(self):
        return "{}: {} - {}".format(self.id, self.node1, self.node2)
 
    def is_same(self, link):
        if link is None:
            return False
        elif (int(self.node1) == int(link.node1) and int(self.node2) == int(link.node2)) or \
            (int(self.node1) == int(link.node2) and int(self.node2) == int(link.node1)):
            return True
        else:
            return False

    def has_node(self, node):
        if int(self.node1) == int(node) or int(self.node2) == int(node):
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
        for old_link in self.links:
            if old_link.is_same(new_link):
                return
        self.links.append(new_link)

    def find_link(self, link):
        for my_link in self.links:
            if my_link.is_same(link):
                return my_link
        return None

    def get_connected_links(self, node):
        links = []
        for link in self.links:
            if link.has_node(node):
                links.append(link)
        return links
    
    def get_link(self, id):
        return self.links[id]

    def get_id(self):
        return len(self.links)

    def length(self):
        return len(self.links)

def generate_links_from_file(filename):
    f = open(filename, 'r')
    links = LinkSet()
    for line in f.readlines():
        nodes = line.split("-")
        links.add_link(Link(links.get_id(), nodes[0].strip(), nodes[1].strip()))
    return links

def generate_complete_graph(nodes):
    links = LinkSet()
    for index, node1 in enumerate(nodes):
        for node2 in nodes[index+1:]:
            links.add_link(Link(links.get_id(), node1, node2))
    return links

def auto_generate_sparse_graph(nodes, additional_links_count=0):
    # 讓每個節點都要連到其他任意一個節點 (先長一棵tree)
    links = LinkSet()
    in_tree_nodes = [nodes[0]]
    for node in nodes[1:]:
        if node not in in_tree_nodes:
            connect_node = random.choice(in_tree_nodes)
            links.add_link(Link(links.get_id(), node, connect_node))
            in_tree_nodes.append(node)

    # 再隨意找幾個點多連幾條link
    chosen_additional_nodes = []
    for i in range(additional_links_count):
        temp_additional_nodes = random.sample(nodes, 1)
        chosen_additional_nodes.extend(temp_additional_nodes)
    for node in chosen_additional_nodes:
        # 找到另外一個點，並確保這個link尚未在links中
        connect_node = random.choice(nodes)
        while node is connect_node or links.find_link(Link(0, node, connect_node)) is not None:
            connect_node = random.choice(nodes)
        links.add_link(Link(links.get_id(), node, connect_node))
    return links