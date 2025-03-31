# make targets for zmap by inputting a network (doesnt matter if its /32 or /48) and an IID

import ipaddress

def generate_ipv6_addresses(network_block, iid):
    # convert the network block into an ipv6network object
    network = ipaddress.IPv6Network(network_block, strict=False)
    
    # convert the IID into an integer
    iid_int = int(ipaddress.IPv6Address(f"::{(iid)}"))
    
    # iterate over all possible addresses in the network
    for ip in network.hosts():
        # combine the network prefix with the IID
        new_ip = ipaddress.IPv6Address(int(ip) | iid_int)
        print(new_ip)

if __name__ == "__main__":
    network_block = input("Network: ").strip()
    iid = input("IID: ").strip()
    generate_ipv6_addresses(network_block, iid)