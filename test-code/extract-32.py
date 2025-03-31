#go through a file of IPv6 addresses and extract the first 32 bits of each address.
#only gets the unique ones

import bz2
import re

input_file = "../RawData/ntp-2025-01-26-high-entropy-full-addresses.txt.bz2"
output_file = "../Data/unique_ipv6_prefixes.txt"

# regular expression to match IPv6 addresses
ipv6_pattern = re.compile(r'([0-9a-fA-F:]+)')

# function to extract the first 32 bits from an ipv6 address
def extract_ipv6_prefix(ipv6_address):
    parts = ipv6_address.split(":")  # split ipv6 address by :
    prefix = ":".join(parts[:2])  # extract the first 32 bits 
    return prefix + "::/32"  # return standardized /32 prefix

# set to store unique /32 prefixes
unique_prefixes = set()

# open and process the compressed file
with bz2.BZ2File(input_file, "rb") as file:
    for line in file:
        line = line.decode("utf-8").strip()  # decode binary to string
        match = ipv6_pattern.search(line)  # find an ipv6 address in the line
        if match:
            ipv6 = match.group(1)
            prefix = extract_ipv6_prefix(ipv6)  # get the /32 prefix
            unique_prefixes.add(prefix)  # store unique prefixes

# write unique /32 prefixes to the output file
with open(output_file, "w") as output:
    for prefix in sorted(unique_prefixes):
        output.write(prefix + "\n")

print(f"Unique /32 prefixes saved to {output_file}")
