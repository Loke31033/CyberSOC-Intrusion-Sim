import os
import re
import json
from collections import defaultdict

# Handles ISO format and traditional syslog formats
def extract_timestamp_and_message(line):
    # ISO Format: 2025-05-26T11:18:22.162296+00:00 hostname process: message
    if re.match(r"^\d{4}-\d{2}-\d{2}T", line):
        try:
            timestamp, rest = line.split(" ", 1)
            return timestamp, rest.strip()
        except:
            return "", line.strip()
    # Syslog format: Jul 31 11:22:53 hostname process: message
    elif re.match(r"^[A-Z][a-z]{2} +\d{1,2} \d{2}:\d{2}:\d{2}", line):
        try:
            parts = line.split(" ", 4)
            timestamp = " ".join(parts[:3])
            message = parts[4] if len(parts) > 4 else ""
            return timestamp, message.strip()
        except:
            return "", line.strip()
    else:
        return "", line.strip()

def detect_bruteforce(events):
    failed_logins = defaultdict(int)
    attacker_ips = set()
    findings = []

    for ts, msg in events:
        match = re.search(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)", msg)
        if match:
            ip = match.group(1)
            failed_logins[ip] += 1
            if failed_logins[ip] >= 3:
                findings.append(f"🔴 Brute-force detected from {ip} with {failed_logins[ip]} failed attempts")
                attacker_ips.add(ip)

    return findings, list(attacker_ips)

def main():
    log_dir = "logs"
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    events = []
    for fname in os.listdir(log_dir):
        if fname.endswith(".log"):
            with open(os.path.join(log_dir, fname), "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "Failed password" in line or "Accepted password" in line:
                        ts, msg = extract_timestamp_and_message(line.strip())
                        if ts:
                            events.append((ts, msg))

    findings, attacker_ips = detect_bruteforce(events)

    # Write timeline.csv
    with open(os.path.join(output_dir, "timeline.csv"), "w") as f:
        f.write("Timestamp,Description\n")
        for ts, msg in events:
            f.write(f"{ts},{msg}\n")

    # Write iocs.json
    iocs = {
        "attacker_ips": attacker_ips,
        "compromised_users": list(set(re.findall(r"Accepted password for (\w+)", "\n".join([e[1] for e in events])))),
        "targets": list(set(re.findall(r"from (\d+\.\d+\.\d+\.\d+)", "\n".join([e[1] for e in events]))))
    }
    with open(os.path.join(output_dir, "iocs.json"), "w") as f:
        json.dump(iocs, f, indent=4)

    # Write findings.txt
    with open(os.path.join(output_dir, "findings.txt"), "w") as f:
        for finding in findings:
            f.write(f"{finding}\n")

    print(f"[✓] Parsed {len(events)} events")
    print(f"[✓] Correlations found: {len(findings)}")
    print(f"[✓] Wrote: {output_dir}/timeline.csv")
    print(f"[✓] Wrote: {output_dir}/iocs.json")
    print(f"[✓] Wrote: {output_dir}/findings.txt")

if __name__ == "__main__":
    main()

