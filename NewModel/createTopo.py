from logging import error
from mininet.net import Mininet
from mininet.node import Node, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.util import macColonHex
import pandas as pd
import pickle

import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ETH_IPV4 = 2048
ETH_ARP = 2054
NUM_NODES = 20
setLogLevel('info')


def int2dpid(dpid):
    try:
        dpid = hex(dpid)[2:]
        dpid = '0' * (16-len(dpid)) + dpid
        return dpid
    except IndexError:
        return Exception('Dpi failed: '+dpid)


def addFlowEntry(switches):
    s = requests.session()
    s.auth = ('sdbox', 'sdbox')
    s.verify = False

    while 1:
        time.sleep(5)
        resp = s.get(
            'https://192.168.11.232/api/openflow/switch/').json()
        print('Get switch info')
        print(resp)
        try:
            for i in range(1, NUM_NODES+1):
                nodeName = str(i)
                for sw in resp:
                    if i == sw['dpid']:
                        switches[nodeName]['id'] = sw['id']
                print(f"s{nodeName}: {switches[nodeName]['id']}")
        except:
            continue
        break

    print('Add flow entry', end='...')
    data = []
    for i in range(1, NUM_NODES+1):
        nodeName = str(i)
        data.append({
            'sw': switches[nodeName]['id'],
            'priority': 1000,
            'table_id': 1,
            'match': {
                'eth_type': ETH_IPV4,
                'ipv4_dst': switches[nodeName]['host'].IP(),
            },
            'actions': [
                {
                    'type': 'OUTPUT',
                    'port': 1,
                },
            ],
            'groups': 1,
            'is_permanent': True
        })
        data.append({
            'sw': switches[nodeName]['id'],
            'priority': 1000,
            'table_id': 1,
            'match': {
                'eth_type': ETH_ARP,
                'arp_tpa': switches[nodeName]['host'].IP(),
            },
            'actions': [
                {
                    'type': 'OUTPUT',
                    'port': 1,
                },
            ],
            'groups': 1,
            'is_permanent': True
        })
    s.post('https://192.168.11.232/api/openflow/flowentry/', json=data)
    print('DONE!')


def save_obj(obj, name):
    with open('./data/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def main():
    link_df = pd.read_excel('data/topology.xlsx',
                            engine='openpyxl', sheet_name='link', index_col=0)

    # add topo
    net = Mininet(topo=None, build=False, autoSetMacs=True)
    print('create switches: ')
    switches = {}
    switch_adjacency_matrix = {}
    ip = 1
    for i in range(1, NUM_NODES+1):
        nodeName = str(i)
        switch_adjacency_matrix[nodeName] = {}
        print('#s' + nodeName)
        switches[nodeName] = {}
        switches[nodeName]['obj'] = net.addSwitch('s' + nodeName, dpid=int2dpid(
            i), protocols='OpenFlow13', datapath='user', ovs='ovsk')
        switches[nodeName]['host'] = net.addHost(
            'h' + nodeName, ip=f'10.0.1.{ip}', mac=macColonHex(ip), defaultRoute='via 10.0.1.254')
        ip = ip+1
        net.addLink(switches[nodeName]['obj'],
                    switches[nodeName]['host'], port1=1, port2=1)
        switches[nodeName]['unused'] = 2

    print('create switches links: ')
    for index, row in link_df.iterrows():
        node1Name = str(row[' node1'])
        node2Name = str(row[' node2'])

        fromNode = switches[node1Name]
        toNode = switches[node2Name]
        bw = row[' bandwidth']
        print(node1Name + ' to ' + node2Name + ' (' + str(bw), end=')...')

        net.addLink(fromNode['obj'], toNode['obj'],
                    port1=fromNode['unused'], port2=toNode['unused'], bw=bw)
        switch_adjacency_matrix[node1Name][node2Name] = fromNode['unused']
        switch_adjacency_matrix[node2Name][node1Name] = toNode['unused']

        fromNode['unused'] = fromNode['unused'] + 1
        toNode['unused'] = toNode['unused'] + 1
        print('Completed!')

    print('create controllers')
    ctrl_1 = net.addController(
        'c1', controller=RemoteController, ip='192.168.11.232', port=6633)
    net.staticArp()
    net.build()

    for s in net.switches:
        s.start([ctrl_1])

    save_obj(switch_adjacency_matrix, 'switch-adjacency-matrix')
    addFlowEntry(switches)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    main()
