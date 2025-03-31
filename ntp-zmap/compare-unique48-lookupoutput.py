# Compare the list of unique /48s I made, from the full /64 addresses that have repeated IIDs 
# with the output from lookup.py which compared the list of ipv6 addresses with a rib file

import sys

def load_short_list(file_path):
    """Load the short /48 list into a set for fast lookup."""
    with open(file_path, "r") as f:
        return set(line.strip() for line in f)

def match_ipv6(short_list, long_file, output_file):
    """Find and save matching entries from the long list."""
    with open(long_file, "r") as f, open(output_file, "w") as out_f:
        for line in f:
            parts = line.strip().split(",")  # split into IPv6, /48, ASN
            if len(parts) < 2:
                continue  # skip malformed lines
            
            ipv6_prefix = parts[1]  # extract the /48 prefix
            
            if ipv6_prefix in short_list:
                out_f.write(line)  # write matching lines to output

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 match_ipv6.py short_list.txt long_list.txt output.txt")
        sys.exit(1)

    short_list_file = sys.argv[1]
    long_list_file = sys.argv[2]
    output_file = sys.argv[3]

    # load the short /48 list
    short_list = load_short_list(short_list_file)

    # match and write results
    match_ipv6(short_list, long_list_file, output_file)

    print(f"Matching entries written to {output_file}")
