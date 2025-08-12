import json
from collections import Counter

def load_events(path="logs/alerts.jsonl"):
    events = []
    try:
        with open(path, "r") as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except Exception:
                    pass
    except FileNotFoundError:
        print("No logs found yet. Run the honeypot first.")
    return events

def summary(events):
    kinds = Counter(e["kind"] for e in events)
    ips = Counter(e.get("meta", {}).get("ip", "unknown") for e in events if "meta" in e)
    ports = Counter(e.get("meta", {}).get("port", "unknown") for e in events if "meta" in e)
    return kinds, ips, ports

if __name__ == "__main__":
    ev = load_events()
    kinds, ips, ports = summary(ev)
    print("=== HoneyWatch Summary ===")
    print("By type:", kinds)
    print("Top IPs:", ips.most_common(10))
    print("Ports:", ports)
