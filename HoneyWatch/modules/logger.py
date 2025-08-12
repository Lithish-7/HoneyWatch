import json
from datetime import datetime

class Reporter:
    def __init__(self, log_path="logs/alerts.log", json_path="logs/alerts.jsonl"):
        self.log_path = log_path
        self.json_path = json_path

    def alert(self, kind, message, meta=None):
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        line = f"[{ts}] [{kind}] {message}"
        with open(self.log_path, "a") as f:
            f.write(line + "\n")
        with open(self.json_path, "a") as f:
            f.write(json.dumps({"ts": ts, "kind": kind, "message": message, "meta": meta or {} }) + "\n")
