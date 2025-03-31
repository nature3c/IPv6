# This script takes a list of IPv6 addresses and finds all unique /48 prefixes that match a given IID
# Usage: python3 active-48s.py --input <file> --iid <IID>

import argparse
import ipaddress

def get_prefix(address):
    # return the /48 prefix
    try:
        ip = ipaddress.IPv6Address(address)
        # grab first 3 hextets for /48
        parts = address.split(":")
        full = []
        for part in parts:
            if part == '':
                # expand ::
                missing = 8 - len(parts) + 1
                full.extend(['0000'] * missing)
            else:
                full.append(part.zfill(4))
        return ":".join(full[0:3]) + "::/48"
    except ValueError:
        return None

def get_iid(address):
    # return the last 4 hextets
    parts = address.split(":")
    # pad shortened (::) addresses
    full_parts = []
    for part in parts:
        if part == '':
            missing = 8 - len(parts) + 1
            full_parts.extend(['0000'] * missing)
        else:
            full_parts.append(part.zfill(4))
    return ":".join(full_parts[-4:])

def main():
    parser = argparse.ArgumentParser(description="Find unique /48 prefixes that match a given IID.")
    parser.add_argument("--input", required=True, help="Input file containing IPv6 addresses.")
    parser.add_argument("--iid", required=True, help="IID to match (e.g. 0478:5634:1232:5476).")
    args = parser.parse_args()

    matching_prefixes = set()

    with open(args.input, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue

            iid = get_iid(line)
            if iid.lower() == args.iid.lower():
                prefix = get_prefix(line)
                if prefix:
                    matching_prefixes.add(prefix)

    # save to file
    with open("matching_prefixes.txt", "w") as out:
        for prefix in sorted(matching_prefixes):
            out.write(prefix + "\n")

    print(f"\nSaved {len(matching_prefixes)} unique /48 prefixes to matching_prefixes.txt")

if __name__ == "__main__":
    main()
