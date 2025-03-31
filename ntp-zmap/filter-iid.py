# Removes IIDs from main file that exist in filter file
# I made this because I used the wrong list of IIDs when running iid_scanner.py

import argparse

def filter_iids(main_file, filter_file, output_file):
    # Read IIDs from filter file into a set for fast lookup
    with open(filter_file, 'r') as f:
        filter_iids = {line.strip() for line in f if line.strip()}
    
    # Process main file
    kept_iids = []
    removed_count = 0
    
    with open(main_file, 'r') as f:
        for line in f:
            iid = line.strip()
            if iid and iid not in filter_iids:
                kept_iids.append(iid)
            elif iid:
                removed_count += 1
    
    # Write results
    with open(output_file, 'w') as f:
        f.write('\n'.join(kept_iids) + '\n')
    
    print(f"Filtering complete. Results saved to {output_file}")
    print(f"Original count: {len(kept_iids) + removed_count}")
    print(f"Removed: {removed_count}")
    print(f"Remaining: {len(kept_iids)}")

def main():
    parser = argparse.ArgumentParser(description='Remove IIDs from first file that appear in second file')
    parser.add_argument('--main', required=True, help='Main file containing IIDs to filter')
    parser.add_argument('--filter', required=True, help='File containing IIDs to remove')
    parser.add_argument('--output', required=True, help='Output file for filtered results')
    
    args = parser.parse_args()
    
    filter_iids(args.main, args.filter, args.output)

if __name__ == "__main__":
    main()