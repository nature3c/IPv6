#takes an input file of /32 networks and an input file of ipv6 addresses
#outputs a file of /48 subnets that match the /32 networks

import ipaddress
import bz2
from collections import defaultdict

def extract_48_subnet(ipv6_address):
    """
    extract the /48 subnet from an ipv6 address
    """
    ip = ipaddress.IPv6Address(ipv6_address)
    network = ipaddress.IPv6Network((ip, 48), strict=False)
    return network

def match_32_to_48(networks_32, ipv6_addresses):
    """
    match each /32 to a /48 subnet
    """
    unique_48_subnets = set()

    # get all /48 subnets from the IPv6 addresses
    for ip in ipv6_addresses:
        try:
            subnet_48 = extract_48_subnet(ip)
            unique_48_subnets.add(subnet_48)
        except ipaddress.AddressValueError:
            continue  # Skip invalid IPv6 addresses

    # match each /32 network to the /48 subnets
    matched_48_subnets = set()
    for network_32 in networks_32:
        network_32_obj = ipaddress.IPv6Network(network_32, strict=False)
        for subnet_48 in unique_48_subnets:
            if subnet_48.subnet_of(network_32_obj):
                matched_48_subnets.add(subnet_48)

    return matched_48_subnets

def save_subnets_to_file(subnets, output_file):
    """
    save a list of unique /48 subnets to a text file
    """
    with open(output_file, 'w') as f:
        for subnet in sorted(subnets):
            f.write(f"{subnet}\n")

def read_networks_from_file(file_path):
    """
    read a list of networks from a file. used for the /32 networks
    """
    networks = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  #skip empty lines
                networks.append(line)
    return networks

def read_ipv6_addresses_from_bz2(file_path):
    """
    read a list of ipv6 addresses from a .bz2 file.
    """
    addresses = []
    with bz2.open(file_path, 'rt') as f:
        for line in f:
            line = line.strip()
            if line:  # skip empty lines
                addresses.append(line)
    return addresses

def main():
    networks_32_file = "../Data/unique_ipv6_prefixes.txt"
    ipv6_addresses_bz2_file = "../RawData/ntp-2025-01-26-high-entropy-full-addresses.txt.bz2"
    output_file = "../Data/unique_48.txt"

    networks_32 = read_networks_from_file(networks_32_file)

    ipv6_addresses = read_ipv6_addresses_from_bz2(ipv6_addresses_bz2_file)

    matched_48_subnets = match_32_to_48(networks_32, ipv6_addresses)

    save_subnets_to_file(matched_48_subnets, output_file)

    print(f"Saved {len(matched_48_subnets)} unique /48 subnets to {output_file}")

if __name__ == "__main__":
    main()