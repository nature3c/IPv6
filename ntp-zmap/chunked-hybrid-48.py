# Generate randomized full IPv6 addresses from /48 prefixes and a fixed IID but its randomized!
# But also this will shuffle with an n number of other /48 prefixes for more randomness to avoid traffic being blocked
# Outputs to stdout so I can pipe it to zmap and avoid disc io
# Usage: python3 chunked-hyrbid-48.py --file <file> --iid <IID> | probably zmap

import argparse
import ipaddress
import random
import sys

ADDR_COUNT = 65536  # /64s in a /48
CHUNK_SIZE = 15      # number of /48s to load and shuffle together per batch


def parse_iid(iid_str):
    # convert an IID string into a 64-bit integer
    try:
        # try as full ipv6 address
        return int(ipaddress.IPv6Address(iid_str)) & ((1 << 64) - 1)
    except ValueError:
        try:
            # try as IID padded with zeros
            iid_full = f"::{'0:' * 3}{iid_str}"
            return int(ipaddress.IPv6Address(iid_full)) & ((1 << 64) - 1)
        except ValueError:
            raise ValueError(f"Invalid IID format: {iid_str}")


def generate_addresses_from_prefix(prefix_str, iid_int):
    # generate a randomized list of full ipv6 addresses from a /48 prefix and fixed IID
    try:
        # validate and parse the /48 prefix
        if not prefix_str.endswith("/48"):
            print(f"Skipping invalid prefix (not /48): {prefix_str}", file=sys.stderr)
            return []

        network = ipaddress.IPv6Network(prefix_str, strict=False)
        base = int(network.network_address)

        # generate all subnet values and shuffle
        subnets = list(range(ADDR_COUNT))
        random.shuffle(subnets)

        addresses = []
        for subnet in subnets:
            full_addr_int = (base & ((1 << 128) - (1 << 80))) | (subnet << 64) | iid_int
            full_addr = ipaddress.IPv6Address(full_addr_int)
            addresses.append(str(full_addr))
        return addresses

    except ValueError as e:
        print(f"Error processing prefix {prefix_str}: {e}", file=sys.stderr)
        return []


def chunked(iterable, size):
    # yield successive chunks from list
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


def main():
    parser = argparse.ArgumentParser(
        description="Chunked hybrid IPv6 generator from /48 prefixes with a fixed IID"
    )
    parser.add_argument("--file", required=True, help="Input file with /48 prefixes, one per line")
    parser.add_argument("--iid", required=True, help="Fixed Interface Identifier (e.g., ::1)")

    args = parser.parse_args()

    try:
        iid_int = parse_iid(args.iid)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file, 'r') as f:
            all_prefixes = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    # process in chunks of CHUNK_SIZE
    for prefix_group in chunked(all_prefixes, CHUNK_SIZE):
        combined_addresses = []
        for prefix in prefix_group:
            combined_addresses.extend(generate_addresses_from_prefix(prefix, iid_int))

        # global shuffle across this chunk
        random.shuffle(combined_addresses)

        for addr in combined_addresses:
            print(addr)


if __name__ == "__main__":
    main()
