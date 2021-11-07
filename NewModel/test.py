from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info


def treeNet():
    # Create a tree network without a local controller and constrained links
    net = Mininet(link=TCLink, build=False, ipBase='10.0.0.0/8')

    # Adding remote controller
    net.addController('c1')

    # Adding hosts
    h1a = net.addHost('h1a', ip='10.0.0.1')
    h2p = net.addHost('h2p', ip='10.0.0.2')
    h3p = net.addHost('h3p', ip='10.0.0.3')
    h4p = net.addHost('h4p', ip='10.0.0.4')

    # Adding switches
    s1 = net.addSwitch('s1', protocols='OpenFlow13',
                       datapath='user', ovs='ovsk')
    s2 = net.addSwitch('s2', protocols='OpenFlow13',
                       datapath='user', ovs='ovsk')
    s3 = net.addSwitch('s3', protocols='OpenFlow13',
                       datapath='user', ovs='ovsk')

    # Creating core links 100Mbps, 100ms delay and user links 1000Mbps and 1ms delay
    net.addLink(h1a, s2, port1=1, port2=2)
    net.addLink(h2p, s2, port1=1, port2=3)
    net.addLink(s2, s1, bw=100, delay='100ms')
    net.addLink(s3, s1, bw=100, delay='100ms')
    net.addLink(h3p, s3, bw=1000, delay='1ms')
    net.addLink(h4p, s3, bw=1000, delay='1ms')

    net.build()
    # Starting network
    net.start()

    # Dumping host connections
    dumpNodeConnections(net.hosts)

    # Testing network connectivity
    # net.pingAll()

    # Testing bandwidth between nodes
    # h1a, h2p = net.get('h1a', 'h2p')
    # net.iperf((h1a, h2p))

    # h2p, h1a = net.get('h2p', 'h1a')
    # net.iperf((h2p, h1a))

    # h2p, h3p = net.get('h2p', 'h3p')
    # net.iperf((h2p, h3p))

    # h2p, h4p = net.get('h2p', 'h4p')
    # net.iperf((h2p, h4p))

    # h3p, h4p = net.get('h3p', 'h4p')
    # net.iperf((h3p, h4p))

    # Running CLI
    CLI(net)

    # Stopping network
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    treeNet()
