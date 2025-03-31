# takes a list of inputs that look like "151636  | 2400:a560:c04b:0000:f95a:82b0:86b7:f534  | RELIANCE-AS-AP Reliance Broadband, PK"
# and counts the number of unique ASNs and countries in the list, then writes the counts to two separate csv files

import sys
from collections import defaultdict

def count_asn_and_countries(input_file, asn_output_file, country_output_file):
    asn_counts = defaultdict(int)
    country_counts = defaultdict(int)

    with open(input_file, "r") as f:
        for line in f:
            parts = line.strip().split("|")  # split by |
            if len(parts) < 3:
                continue  # skip malformed lines
            
            asn_info = parts[2].strip()
            if "," in asn_info:
                asn_name, country = asn_info.rsplit(",", 1)  # split asn name and country
                asn_name = asn_name.strip()
                country = country.strip()
                
                asn_counts[asn_name] += 1
                country_counts[country] += 1

    # write asn counts to a csv file
    with open(asn_output_file, "w") as asn_f:
        asn_f.write("ASN,Count\n")  # csv Header
        for asn, count in sorted(asn_counts.items(), key=lambda x: -x[1]):
            asn_f.write(f"{asn},{count}\n")

    # write country counts to a csv file
    with open(country_output_file, "w") as country_f:
        country_f.write("Country,Count\n")  # csv header
        for country, count in sorted(country_counts.items(), key=lambda x: -x[1]):
            country_f.write(f"{country},{count}\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python count_asn_country.py input.txt asn_counts.csv country_counts.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    asn_output_file = sys.argv[2]
    country_output_file = sys.argv[3]

    count_asn_and_countries(input_file, asn_output_file, country_output_file)
    print(f"Results saved to {asn_output_file} and {country_output_file}")
