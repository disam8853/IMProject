# code for generate virtual switches use mininet

from catknight import *
import pandas as pd
import json
import sys
import time

def myCatknight(adj_path, link_path, method_path, method):
    try:
        start_time = time.time()
        topo = Catknight(auth=('sdbox','sdbox'), clean = False)
        if method == "-d": 
            topo.deleteAll()
            quit()
        prepand = "n"
        # nodes = ['a', 'b', 'c']
        # adj = pd.read_csv("../IMProject/DeployModel/code/adjacency.csv")
        adj = pd.read_csv(adj_path)
        nodes = [prepand + str(i) for i in range(adj.shape[0])]
        del adj

        # links = [('a','b'),('b','c')]
        # df = pd.read_csv("../IMProject/DeployModel/code/link.csv")
        df = pd.read_csv(link_path)
        # links = [(prepand + str(df["origin"][i]), prepand + str(df["destination"][i])) for i in range(df.shape[0])]
        links = []
        for i in range(df.shape[0]):
            b = 0
            for obj in links:
                if (prepand + str(df["destination"][i]), prepand + str(df["origin"][i])) == obj:
                    b = 1
                    break
            if not b:
                links.append((prepand + str(df["origin"][i]), prepand + str(df["destination"][i])))
        print(links)
        del df
        net = topo.feed(nodes, links)
        
        # topo.addPath(['a','b','c'])
        # topo.addPath(['c','b','a'])
        # "../IMProject/DeployModel/code/path/result.json"
        with open(method_path, "r") as jsonfile:
            jsdata = json.load(jsonfile)
        startID = jsdata[list(jsdata.keys())[0]]['link'][0]
        destID = jsdata[list(jsdata.keys())[0]]['link'][-1]
        
        for key in jsdata.keys():
            
            link_len = len(jsdata[key]['link'])
            linkset = []
            for link_idx in range(link_len):
                linkset.append(prepand + str(jsdata[key]['link'][link_idx]))
            print(key, linkset)
            print(key, linkset[::-1])
            topo.addPath(linkset)
            topo.addPath(linkset[::-1])
        iter_times = 3600
        cost_time = time.time() - start_time
        print("\n ~~~ Create Cost: {} min {} secs ~~~\n".format(int(cost_time/60), cost_time%60))
        start_time = time.time()

        if method == "run":
            for i in range(iter_times):
                time.sleep(0.5)
                topo.ping("n" + str(startID), "n" + str(destID))
            while len(sys.argv) > 1:
                ping = input("{} ping {}? (Y/N)".format(startID, destID))
                if ping == "Y" or ping == "y":
                    iter_times = 10
                    for i in range(iter_times):
                        time.sleep(1)
                        topo.ping("n" + str(startID), "n" + str(destID))
                elif ping == "N" or ping == "n":
                    print("Bye bye")
                else:
                    print("Please enter Y or N.")
                    continue
        elif method == None:
            CLI(net)
        cost_time = time.time() - start_time
        print("\n ~~~ Cost: {} min {} secs ~~~\n".format(int(cost_time/60), cost_time%60))
        
    except Exception as e:
        print(e)
        return e
if len(sys.argv) > 1:
    myCatknight("./adjacency.csv", "./link.csv", "./path/result.json", sys.argv[1])
else:
    myCatknight("./adjacency.csv", "./link.csv", "./path/result.json", None)
    
