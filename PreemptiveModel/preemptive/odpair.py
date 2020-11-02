from link import Link, LinkSet
from config import traffic, routing_num, minDelayTol_w, maxDelayTol_w
import copy
import random        
import numpy as np
import math

class Path():
    def __init__(self, id=0, node_list=[], link_list=[]):
        self.id = id
        self.node_list = node_list
        self.link_list = link_list  
    def __str__(self):
        #return str(self.id) + ": " + str(self.node_list)
        return str(self.node_list)
    
    def add_node(self, node):
        self.node_list.append(node)
    
    def add_link(self, link):
        self.link_list.append(link)

    def has_link(self, link: Link):
        for node1, node2 in zip(self.node_list[:-1], self.node_list[1:]):
            if link.is_same(Link(0, node1, node2)):
                return True
        return False
    
    
    
class ODpair():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.delayTol = random.uniform(minDelayTol_w,maxDelayTol_w)
        self.traffic = traffic
        self.paths = []
        
        
    def __str__(self):
        string = str(self.start) + " -> " + str(self.end) + "\n" 
        for path in self.paths:
            string += str(path) + "\n"
        return string
    
    def get_pathset(self):
        return self.paths
        
    def add_path(self, path: Path):
        if path.node_list[0] == self.start and path.node_list[-1] == self.end:
            self.paths.append(path)
    
    def generate_path(self, link_set):
        path = Path(node_list=[self.start])
        src_outgoing_links = link_set.get_connected_links(self.start)
        #src_outgoing_links = random.sample(src_outgoing_links,3) #避免找到非常相似的可能路徑
        self.find_path(path, src_outgoing_links, link_set)

    def find_path(self, path: Path, outgoing_links: list, link_set: LinkSet):
        #count = 0
        if path.node_list[-1] == self.end:
            self.add_path(path)
        else:
            for outgoing_link in outgoing_links:
                '''
                count +=1
                if count >= 3:
                    break
                '''
                if(len(path.node_list)>routing_num):
                    break
                new_node = outgoing_link.node1 if path.node_list[-1] is outgoing_link.node2 else outgoing_link.node2
                if new_node not in path.node_list:
                    new_path = copy.deepcopy(path)
                    new_path.add_node(new_node)
                    new_path.add_link(outgoing_link)    
                    new_outgoing_links = copy.deepcopy(link_set.get_connected_links(new_node))
                    #new_outgoing_links = random.sample(new_outgoing_links,3) #避免找到非常相似的可能路徑
                    for link in new_outgoing_links:
                        if link.is_same(outgoing_link):
                            new_outgoing_links.remove(link)
                            break                
                    self.find_path(new_path, new_outgoing_links, link_set)                
