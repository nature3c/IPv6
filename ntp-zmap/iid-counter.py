#make IID records with entropy values so it looks like
#count, IID

import ipaddress
import bz2
from collections import defaultdict
from pyentrp import entropy as ent

input_file = "../RawData/2024-10-29-ips.txt.bz2" 
output_file = "../Data/entropyfreq_test.txt"

line_limit = 2000000 #line limit so code works

iid_stats = defaultdict(int) #dictionary to track IID count

entropy_threshold = 2.5 #only record IIDs with an entropy higher than this

entropy_cache = {} #cache to store entropy of IIDs

def is_eui64(iid): #looks for ff:fe 
    parts = iid.split(':')
    if len(parts) == 4:
        second_section = parts[1].lower()
        third_section = parts[2].lower()
        return second_section.endswith('ff') and third_section.startswith('fe')
    return False

with bz2.open(input_file, 'rt') as f:
    for i, line in enumerate(f):
        if i >= line_limit: #stop after reaching limit
            break

        l = line.strip()
        try:
            ip = ipaddress.IPv6Address(l)

            last_64_bits = ip.exploded.split(':')[-4:] #last 64 bits
            last_64_str = ':'.join(last_64_bits) #join segments for the full exploded IID

            if is_eui64(last_64_str): #check if its a eui64
                continue
            
            #check entropy cache before calculating (to save time)
            if last_64_str in entropy_cache:
                entropy = entropy_cache[last_64_str]
            else:
                entropy = ent.shannon_entropy(last_64_str.replace(":", "")) #calculate entropy without colons
                entropy_cache[last_64_str] = entropy #store in cache b/c its not in it

             #only count the IID if entropy is higher than 2.5
            if entropy > entropy_threshold:
                iid_stats[last_64_str] += 1
        except ipaddress.AddressValueError:
            continue #ignore invalid addresses

#filter and sort by highest count
filtered_sorted_iid_stats = sorted(
    ((iid, count) for iid, count in iid_stats.items() if count > 5),
    key = lambda x: x[1], #sort by count (second item in tuple)
    reverse = True #descending order
)

#write stuff out to the file
with open(output_file, 'w') as out_f:
    if not filtered_sorted_iid_stats:
        out_f.write("No high entropy IIDs with count > 5 found\n")
        print(" No high-entropy IIDs with count > 5 found")
    else:
        for iid, count in filtered_sorted_iid_stats:
            out_f.write(f"{count},{iid}\n")

print(f"Done!")