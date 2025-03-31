# This script scans takes all the /48s from a list of IIDs from NTP
# and then creates all possible /64s from those /48s. Then it is run
# through ZMap to find active hosts. Then results are counted and
# sorted so that it looks like IID, Count

import subprocess
import os
from datetime import datetime
import argparse

# Command line arguments
parser = argparse.ArgumentParser(description="Scan IPv6 /64s generated from IIDs using ZMap.")
parser.add_argument("--iids", required=True, help="File containing list of IIDs (one per line).")
parser.add_argument("--input", required=True, help="File containing full IPv6 addresses.")
args = parser.parse_args()

# Output folders
PREFIX_DIR = "prefixes"
TARGET_DIR = "targets"
ZMAP_DIR = "zmap_results"
SUMMARY_FILE = "iid_hit_summary.csv"

# ZMap command and settings
ZMAP_BINARY = "sudo zmap"
ZMAP_ARGS = [
    "--probe-module=icmp6_echoscan",
    "-O", "csv",
    "-f", "saddr,outersaddr,ttl,ipid,type,code,icmp-id,seq,timestamp_ts",
    "-r", "10000",
    "--ipv6-source-ip=2604:2dc0:202:300::165e",
    "--output-filter=success=1 && repeat=0"
]

# Make sure folders exist
os.makedirs(PREFIX_DIR, exist_ok=True)
os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(ZMAP_DIR, exist_ok=True)

# Create summary file if missing
if not os.path.exists(SUMMARY_FILE):
    with open(SUMMARY_FILE, "w") as f:
        f.write("IID,Hits\n")

# Load IIDs
with open(args.iids) as f:
    iids = [line.strip() for line in f if line.strip()]

# Process each IID
for iid in iids:
    print(f"\nProcessing IID: {iid}")

    tag = iid.replace(":", "")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    prefix_file = f"{PREFIX_DIR}/prefixes_{tag}.txt"
    target_output = f"{TARGET_DIR}/targets_{tag}.txt"
    zmap_output = f"{ZMAP_DIR}/zmap_{tag}_{timestamp}.csv"

    # Step 1: Find matching /48s
    subprocess.run([
        "python3", "active-48s.py",
        "--input", args.input,
        "--iid", iid
    ])
    os.rename("matching_prefixes.txt", prefix_file)

    # Step 2: Generate /64s with IID
    with open(target_output, "w") as out_f:
        subprocess.run([
            "python3", "chunked-hyrbid-48.py",
            "--file", prefix_file,
            "--iid", iid
        ], stdout=out_f)

    # Step 3: Run ZMap
    print(f"Scanning {iid} with ZMap...")
    with open(target_output) as targets:
        subprocess.run(
            [*ZMAP_BINARY.split(), *ZMAP_ARGS, "--ipv6-target-file=-", "-o", zmap_output],
            stdin=targets
        )

    # Remove the targets file to save space
    os.remove(target_output)

    # Step 4: Count hits
    with open(zmap_output) as zf:
        hit_count = sum(1 for line in zf if not line.startswith("saddr"))

    # Step 5: Record to summary CSV
    with open(SUMMARY_FILE, "a") as f:
        f.write(f"{iid},{hit_count}\n")

    print(f"✅ {hit_count} hosts responded to IID {iid}")