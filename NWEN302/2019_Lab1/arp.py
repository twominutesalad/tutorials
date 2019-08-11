from switchyard.lib.userlib import *
from expiringdict import ExpiringDict

def main(net):
	arp_cache = ExpiringDict(max_len=100, max_age_seconds=10)

	# We're only interesed in listening for ARP on this interface (my WiFi adapter)
	interface = net.interface_by_name("wlp3s0")
	# Define the IP address to be that assigned to "wlp3s0"
	host_ip = interface.ipaddr

	# You can use the expiring dict such as this:
	#arp_cache["key"] = "value"
	#print("Adding a key value pair...")
	#print(cache.get("key"))

	# Basic function to add the mac/ip key value pair to the expiring dict
	def add_arp(packet_obj):
		# In this case the IP is the key, the MAC hardware address is the value
		arp_cache[packet_obj[Arp].senderprotoaddr] = packet_obj[Arp].senderhwaddr

		# Print out the entire dict, for diagnostics
		print(arp_cache)

	# Arp reply function
	def arp_reply(target_ip, target_mac):
		# Create a new Ethernet object. This would be done in link_layer.py for lab1
	    ether = Ethernet()

	    # Set the Ethernet source address to the source address of this hosts Ethernet adapter
	    ether.src = interface.ethaddr

		# Set the Ethernet destination MAC to be target_mac which is passed to this function
	    ether.dst = target_mac

	    # Set the EthernetType to ARP
	    ether.ethertype = EtherType.ARP

	    # Finally, create the ARP request.
	    arp = Arp(operation=ArpOperation.Reply, # Notice this is ArpOperation.Reply
	              senderhwaddr=interface.ethaddr, # This would be done in link_layer.py for lab1
	              senderprotoaddr=interface.ipaddr,
	              targethwaddr=target_mac,
	              targetprotoaddr=target_ip)
	    arp_packet = ether + arp

	    print("Sending...")
	    print(arp_packet)
	    print("\n")
	    net.send_packet(interface, arp_packet)

    # Do forever until the program crashes. Error handling should be added to account for this.
	while True:
		timestamp,input_port,packet = net.recv_packet()
		# Print every packet that comes through the net object
		print(packet[0])

		# If the packet in is of EtherType ARP and is an ArpOperation.Request (as opposed to Reply)..
		# .. then add the IP/MAC pair to the expiring dict / ARP cache. 
		if packet[0].ethertype == EtherType.ARP and packet[Arp].operation == ArpOperation.Request:
			add_arp(packet)
			print("Arp packet received...")
			print ("Received {} on {}".format(packet, input_port))
			print("\n")

			# Finally, if the IP of this host matches the IP requested by the requester, then reply to it..
			# .. using the arp_reply function. 
			if packet[Arp].targetprotoaddr == host_ip:
				arp_reply(packet[Arp].senderprotoaddr, packet[Arp].senderhwaddr)
			#break
		#elif 
		else:
			print("Waiting for ARP packet.")
	net.shutdown()

