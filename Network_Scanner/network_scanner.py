#!/user/bin/env python

import scapy.all as scapy


def scan(ip_addr):
    arp_request = scapy.ARP(pdst=ip_addr)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    # scapy.ls(scapy.ARP())

    srp_answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(srp_answered_list.summary())

    clients_list = []
    for element in srp_answered_list:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(clients_dict)

    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan("192.168.1.1/24")
print_result(scan_result)
