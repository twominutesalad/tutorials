from switchyard.lib.userlib import *

def main(net):
    # Sends out an ARP request to my Vodafone provided router
    
    interface = net.interface_by_name("wlp3s0")
    target_ip = '192.168.1.1'

    ether = Ethernet()
    ether.src = interface.ethaddr
    ether.dst = 'ff:ff:ff:ff:ff:ff'
    ether.ethertype = EtherType.ARP
    arp = Arp(operation=ArpOperation.Request,
              senderhwaddr=interface.ethaddr,
              senderprotoaddr=interface.ipaddr,
              targethwaddr='ff:ff:ff:ff:ff:ff',
              targetprotoaddr=target_ip)
    arppacket = ether + arp

    print(arppacket)

    print("Sending...")
    net.send_packet(interface, arppacket)

    # Then handle an ARP response with arp.py

    net.shutdown()

