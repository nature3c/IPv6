# go through a list of /48s and generate all possible IPv6 addresses

import bz2
import sys

def generate_ipv6_addresses(file_path, iid):
    with bz2.open(file_path, "rt") as f:
        prefixes = [line.strip() for line in f if line.strip()]
    
    ipv6_addresses = []
    for prefix in prefixes:
        for i in range(0x0000, 0x10000):  # iterate from 0000 to FFFF
            ipv6_addresses.append(f"{prefix}:{i:04x}:{iid}")
    
    return ipv6_addresses

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <iid>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    iid = sys.argv[2]
    ipv6_list = generate_ipv6_addresses(file_path, iid)

    output_file = "generated_ipv6_addresses.txt"
    with open(output_file, "w") as out_file:
        out_file.write("\n".join(ipv6_list))
    
    print(f"Generated {len(ipv6_list)} IPv6 addresses and saved to {output_file}")
