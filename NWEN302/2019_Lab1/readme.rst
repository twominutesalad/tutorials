Switchyard
==========

To run the two applications, run:

::

    $ sudo swyard sendpkt.py
    
And:

::

    $ sudo swyard arp.py
    
The sendpkt.py Switchyard program will send a single ARP request out a given interface to a predefined IP address. 

The arp.py Switchyard program will listen for ARP requests, and store IPv4/MAC pairs into an ExpiringDict().

