from switchyard.lib.userlib import *
from expiringdict import ExpiringDict

def main(net):
	arp_cache = ExpiringDict(max_len=100, max_age_seconds=10)

	interface = net.interface_by_name("wlp3s0")
	host_ip = interface.ipaddr

	#arp_cache["key"] = "value"
	#print("Adding a key value pair...")
	#print(cache.get("key"))

	def add_arp(packet_obj):
		arp_cache[packet_obj[Arp].senderprotoaddr] = packet_obj[Arp].senderhwaddr

		print(arp_cache)

	# Arp reply function
	def arp_reply(target_ip, target_mac):
	    ether = Ethernet()
	    ether.src = interface.ethaddr
	    ether.dst = target_mac
	    ether.ethertype = EtherType.ARP
	    arp = Arp(operation=ArpOperation.Reply,
	              senderhwaddr=interface.ethaddr,
	              senderprotoaddr=interface.ipaddr,
	              targethwaddr=target_mac,
	              targetprotoaddr=target_ip)
	    arp_packet = ether + arp

	    print("Sending...")
	    print(arp_packet)
	    print("\n")
	    net.send_packet(interface, arp_packet)

	while True:
		timestamp,input_port,packet = net.recv_packet()
		print(packet[0])
		if packet[0].ethertype == EtherType.ARP and packet[Arp].operation == ArpOperation.Request:
			add_arp(packet)
			print("Arp packet received...")
			print ("Received {} on {}".format(packet, input_port))
			print("\n")
			if packet[Arp].targetprotoaddr == host_ip:
				arp_reply(packet[Arp].targetprotoaddr, packet[Arp].targethwaddr)
			#break
		#elif 
		else:
			print("Waiting for ARP packet.")
	net.shutdown()

