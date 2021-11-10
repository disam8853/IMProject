import numpy as np
import pandas as pd
import json
import requests


def create_switch_adjacency_matrix():
    switch_adjacency_matrix = np.zeros((21, 21))
    r_link = requests.get('https://140.112.106.237:16904/api/openflow/link',
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


switch_adjacency_matrix = create_switch_adjacency_matrix()
r_switch = requests.get('https://140.112.106.237:16904/api/openflow/switch',
                        auth=('sdbox', 'sdbox'), verify=False)
r_link = requests.get('https://140.112.106.237:16904/api/openflow/link',
                      auth=('sdbox', 'sdbox'), verify=False)

if r_switch.status_code == requests.codes.ok:
    print("OK")
    switch_data = json.loads(r_switch.text)
    link_data = json.loads(r_link.text)
    decision = pd.read_excel('./data/decision.xlsx', sheet_name='FCFS')
    f = open('./data/flowentry.txt', 'w')
    f.close()
    for i in range(len(decision)):
        path = decision.loc[i][3]
        path = path.split('-')
        link_priority = decision.loc[i][4]
        if type(link_priority) == str:
            link_priority = link_priority.split(',')
        else:
            link_priority = [link_priority]
        print(path)
        print(link_priority)
        for n in range(len(path)-1):
            node1 = int(path[n])
            node2 = int(path[n+1])
            print(node1, ' to ', node2, ' on ', link_priority[n])
            switch_id = switch_data[node1-1]['id']
            output_port = str(int(switch_adjacency_matrix[node1][node2]))
            origin = decision.loc[i][1]
            origin_ip = switch_data[origin-1]['ip']
            destination = decision.loc[i][2]
            destination_ip = switch_data[destination-1]['ip']
            if link_priority[n] == 1:
                priority = 900
            elif link_priority[n] == 2:
                priority = 800
            elif link_priority[n] == 3:
                priority = 700
            headers = {'Content-Type': 'application/json'}
            params = [{"sw": switch_id, "priority": priority, "match": {"ipv4_src": origin_ip, "ipv4_dst": destination_ip}, "actions": [
                {"type": "OUTPUT", "port": output_port}], "groups": 1, "table_id": 1}]
            r_add_flowentry = requests.post('https://140.112.106.237:16904/api/openflow/flowentry/', auth=(
                'sdbox', 'sdbox'), verify=False, headers=headers, json=params)
            print(params)
            response = json.loads(r_add_flowentry.text)
            # 將新增的 flow entry 記錄在文字檔中
            flow_id = response[0]['id']
            f = open('./data/flowentry.txt', 'a')
            f.write(flow_id + "\n")
            f.close()

            # 執行 mininet 封包轉發

        break

else:
    print(r_switch.status_code, "request error!")

# 查看flow entry是否有正確新增
r_flowentry = requests.get(
    'https://140.112.106.237:16904/api/openflow/flowentry', auth=('sdbox', 'sdbox'), verify=False)
flowentry = json.loads(r_flowentry.text)
for flow in flowentry:
    if flow['priority'] == 900:
        print("YES")

# 刪除此次決策所設定的 flow entry
f = open('./data/flowentry.txt', 'r')
for flow_id in f.readlines():
    flow_id = flow_id.strip()
    r_del_flowentry = requests.delete(
        'https://140.112.106.237:16904/api/openflow/flowentry/'+flow_id+'/', auth=('sdbox', 'sdbox'), verify=False)
f.close()
