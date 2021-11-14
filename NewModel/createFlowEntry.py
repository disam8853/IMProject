import numpy as np
import pandas as pd
import json
import requests
import urllib3
import sys
import pickle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ETH_IPV4 = 2048
ETH_ARP = 2054


def load_obj(name):
    with open('./data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def create_switch_adjacency_matrix():
    switch_adjacency_matrix = np.zeros((21, 21))
    r_link = requests.get('https://192.168.11.232/api/openflow/link',
                          auth=('sdbox', 'sdbox'), verify=False)
    if r_switch.status_code == requests.codes.ok:
        link_data = json.loads(r_link.text)
        for data in link_data:
            port = data['port']
            node1 = port[0]['switch_dpid']
            node1_port = port[0]['port_no']
            node2 = port[1]['switch_dpid']
            node2_port = port[1]['port_no']
            switch_adjacency_matrix[node1][node2] = node1_port
            switch_adjacency_matrix[node2][node1] = node2_port

    return switch_adjacency_matrix


r_switch = requests.get('https://192.168.11.232/api/openflow/switch',
                        auth=('sdbox', 'sdbox'), verify=False)
r_link = requests.get('https://192.168.11.232/api/openflow/link',
                      auth=('sdbox', 'sdbox'), verify=False)
switch_adjacency_matrix = load_obj('switch-adjacency-matrix')

if r_switch.status_code == requests.codes.ok:
    print("GET request is OK")
    switch_data = json.loads(r_switch.text)
    link_data = json.loads(r_link.text)
    decision = pd.read_excel('./data/decision.xlsx',
                             sheet_name='FCFS', engine='openpyxl')
    f = open('./data/flowentry.txt', 'w')
    f.close()
    params = []
    includedFlowEntry = []
    for i in range(len(decision)):
        path = decision.loc[i][3]
        path = path.split('-')
        link_priority = decision.loc[i][4]
        if type(link_priority) == str:
            link_priority = link_priority.split(',')
        else:
            link_priority = [link_priority]
        print(
            f'flow entry: {"->".join(str(x).strip() for x in path)}, priority: {"->".join(str(x).strip() for x in link_priority)} is creating')
        for n in range(len(path)-1):
            node1 = int(path[n])
            node2 = int(path[n+1])
            # print(node1, ' to ', node2, ' on ', link_priority[n])
            switch_id = switch_data[node1-1]['id']
            output_port = switch_adjacency_matrix[str(node1)][str(node2)]
            origin = decision.loc[i][1]
            # origin_ip = switch_data[origin-1]['ip']
            origin_ip = "10.0.1." + path[n].strip()
            destination = decision.loc[i][2]
            # destination_ip = switch_data[destination-1]['ip']
            destination_ip = "10.0.1." + path[n+1].strip()
            if [origin_ip, destination_ip] in includedFlowEntry:
                continue
            else:
                includedFlowEntry.append([origin_ip, destination_ip])
            if link_priority[n] == 1:
                priority = 900
            elif link_priority[n] == 2:
                priority = 800
            elif link_priority[n] == 3:
                priority = 700

            params.append({"sw": switch_id, "priority": priority, "match": {"eth_type": ETH_IPV4, "ipv4_src": origin_ip, "ipv4_dst": destination_ip}, "actions": [
                {"type": "OUTPUT", "port": output_port}], "groups": 1, "table_id": 1})
            params.append({"sw": switch_id, "priority": priority, "match": {"eth_type": ETH_ARP, "arp_spa": origin_ip, "arp_tpa": destination_ip}, "actions": [
                {"type": "OUTPUT", "port": output_port}], "groups": 1, "table_id": 1})

        # 要建立多少path
        # if i > 2:
        #     break
    print(f'{len(params)} flow entries are creating', end='...')
    headers = {'Content-Type': 'application/json'}
    r_add_flowentry = requests.post('https://192.168.11.232/api/openflow/flowentry/', auth=(
        'sdbox', 'sdbox'), verify=False, headers=headers, json=params)
    try:
        response = json.loads(r_add_flowentry.text)
        # 將新增的 flow entry 記錄在文字檔中
        f = open('./data/flowentry.txt', 'a')
        for res in response:
            try:
                f.write(res["id"] + "\n")
            except:
                print(res)
        f.close()
        print('DONE!')
    except:
        f = open('./data/flowentry.txt', 'a')
        f.write(r_add_flowentry.text)
        f.close()
        sys.exit()
    # 執行 mininet 封包轉發


else:
    print(r_switch.status_code, "request error!")

# 查看flow entry是否有正確新增
# r_flowentry = requests.get(
#     'https://192.168.11.232/api/openflow/flowentry/', auth=('sdbox', 'sdbox'), verify=False)
# flowentry = json.loads(r_flowentry.text)
# for flow in flowentry:
#     if flow['priority'] == 900:
#         print("YES")

print("press any key to delete all flow entry...", end='')
input()
# 刪除此次決策所設定的 flow entry
f = open('./data/flowentry.txt', 'r')
for flow_id in f.readlines():
    flow_id = flow_id.strip()
    r_del_flowentry = requests.delete(
        'https://192.168.11.232/api/openflow/flowentry/'+flow_id+'/', auth=('sdbox', 'sdbox'), verify=False)
    print(f'flow entry {flow_id} is deleted')
f.close()
