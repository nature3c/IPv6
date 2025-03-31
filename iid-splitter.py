# Takes a large list of IIDs and splits it into multiple files with nearly equal distribution

import argparse
import math
import os

def split_iids_into_files(input_filename, num_parts=10):
    # Read all IIDs from the input file
    with open(input_filename, 'r') as f:
        iids = [line.strip() for line in f if line.strip()]
    
    total_iids = len(iids)
    print(f"Found {total_iids} IIDs in the input file.")
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    
    # Calculate how many IIDs should go in each file
    base_size = total_iids // num_parts
    remainder = total_iids % num_parts
    
    # Split the IIDs into parts
    start = 0
    for part in range(1, num_parts + 1):
        # Calculate end index for this part
        end = start + base_size + (1 if part <= remainder else 0)
        
        # Get the IIDs for this part
        part_iids = iids[start:end]
        
        # Create the output filename
        output_filename = f"{base_name}_{part}.txt"
        
        # Write this part to file
        with open(output_filename, 'w') as f:
            f.write('\n'.join(part_iids) + '\n')
        
        print(f"Created {output_filename} with {len(part_iids)} IIDs")
        
        # Update start for next iteration
        start = end

def main():
    parser = argparse.ArgumentParser(description='Split a file of IIDs into multiple nearly equal parts')
    parser.add_argument('--input', required=True,
                       help='Path to the input file containing IIDs (one per line)')
    parser.add_argument('--num_parts', type=int, default=10,
                       help='Number of files to split into (default: 10)')
    
    args = parser.parse_args()
    
    split_iids_into_files(args.input, args.num_parts)

if __name__ == "__main__":
    main()