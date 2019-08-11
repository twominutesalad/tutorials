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
    target_ip = '192.168.1.14'

    # Create a new Ethernet object. This would be done in link_layer.py for lab1
    ether = Ethernet()

    # Set the Ethernet source address to the source address of this hosts Ethernet adapter
    ether.src = interface.ethaddr

    # Set the L2 destination to broadcast
    ether.dst = 'ff:ff:ff:ff:ff:ff'

    # Set the EthernetType to ARP
    ether.ethertype = EtherType.ARP

    # Finally, create the ARP request.
    arp = Arp(operation=ArpOperation.Request,
              senderhwaddr=interface.ethaddr, # This would be done in link_layer.py for lab1
              senderprotoaddr=interface.ipaddr,
              targethwaddr='ff:ff:ff:ff:ff:ff',
              targetprotoaddr=target_ip)
    arppacket = ether + arp

    print(arppacket)

    print("Sending...")

    # Finally, send the packet out the physical interface. 
    net.send_packet(interface, arppacket)

    # Then handle the ARP reply with arp.py

    # Gracefully close the net object. 
    net.shutdown()

