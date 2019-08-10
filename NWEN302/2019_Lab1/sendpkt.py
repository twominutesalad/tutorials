# First, you need to import Switchyard:
from switchyard.lib.userlib import *

# Create the main function from which your Switchyard program will be run:
def main(net):
    # Sends out an ARP request to my Vodafone provided router. 
    # net.interface_by_name takes my WiFi adapters name as an input
    # The target IP in this case is hardcoded, as my gateway IP at home won't change.
    # If you wanted to, you could build a utility to send out ARP requests..
    # .. to a large range of addresses in advance. In an actual deployment..
    # .. this might create a lot of overhead traffic.  
    interface = net.interface_by_name("wlp3s0")
    target_ip = '192.168.1.1'

    # Create a new Ethernet object
    ether = Ethernet()

    # Set the Ethernet source address to the source address of this hosts Ethernet adapter
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

