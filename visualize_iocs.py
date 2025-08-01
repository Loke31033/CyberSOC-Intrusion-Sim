import json
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# --- Load IOC data ---
with open("reports/iocs.json", "r") as f:
    iocs = json.load(f)

print("\n[+] Indicators of Compromise (IOCs):")
for ioc in iocs:
    print(f"- {ioc}")

# --- Load timeline data ---
timestamps = []
descriptions = []

with open("reports/timeline.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
            descriptions.append(row["description"])
        except:
            continue

# --- Plot timeline ---
if timestamps:
    plt.figure(figsize=(12, 4))
    plt.plot(timestamps, range(len(timestamps)), marker="o", linestyle="-", color="red")
    plt.title("Attack Timeline")
    plt.xlabel("Time")
    plt.ylabel("Events")
    plt.yticks(range(len(timestamps)), descriptions)
    plt.tight_layout()
    plt.grid(True)
    plt.show()
else:
    print("\n[!] No events found in timeline.csv. Try re-checking your logs.")
