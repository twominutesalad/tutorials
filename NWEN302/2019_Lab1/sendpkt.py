from switchyard.lib.userlib import *

def main(net):
#     eth = Ethernet(dst='ff:ff:ff:ff:ff:ff')
#     ip = IPv4(dst='192.168.1.1', ttl=16, protocol=IPProtocol.ICMP)
#     icmp = ICMP(icmptype=ICMPType.EchoRequest)
#     icmp.icmpdata.sequence = 1
#     icmp.icmpdata.identifier = 13

#     #eth.src = 'ff:ff:ff:ff:ff:ff'

#     pkt = Packet()

#     pkt += eth
#     pkt += ip
#     pkt += icmp

    # Sends out an ARP request to my Vodafone provided router
    
    interface = net.interface_by_name("wlp3s0")
    targetip = '192.168.1.1'

    ether = Ethernet()
    ether.src = interface.ethaddr
    ether.dst = 'ff:ff:ff:ff:ff:ff'
    ether.ethertype = EtherType.ARP
    arp = Arp(operation=ArpOperation.Request,
              senderhwaddr=interface.ethaddr,
              senderprotoaddr=interface.ipaddr,
              targethwaddr='ff:ff:ff:ff:ff:ff',
              targetprotoaddr=targetip)
    arppacket = ether + arp

    print(arppacket)

    print("Sending...")
    net.send_packet(interface, arppacket)

    # Then handle an ARP response






#     print("Packet format: " + str(pkt))


#     for intf in net.interfaces():
#         eth.src = intf.ethaddr
#         ip.src = intf.ipaddr
#         print("Sending {} out {}".format(pkt, intf.name))
#         try:
#             net.send_packet(intf.name, pkt)
#             print("Sending...")
#             print(pkt)
#         except Exception as e:
#             log_failure("Can't send packet: {}".format(str(e)))
    net.shutdown()



# def main(net):
#     for intf in net.interfaces():
#         log_info("{} has ethaddr {} and ipaddr {}/{} and is of type {}".format(
#             intf.name, intf.ethaddr, intf.ipaddr, intf.netmask, intf.iftype.name))
