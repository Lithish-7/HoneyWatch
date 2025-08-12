# 🐝 HoneyWatch — Honeypot + Visualizer (MVP)

**HoneyWatch** is a low‑interaction honeypot that listens on multiple ports (22/23/80 by default), logs connections & payloads, and saves them to both a human log and JSONL. Includes a **local dashboard** that visualizes alerts by type, IP, and port — all client‑side (no server required).

## ✨ Features
- Multi‑port honeypot using asyncio (22/23/80 by default)
- Fake service **banners** per port (SSH/Telnet/HTTP)
- Logs to `logs/alerts.log` and `logs/alerts.jsonl`
- **Zero‑backend dashboard** in `web/index.html` (drop the JSONL file to visualize)
- Minimal config via `config.json`

> ⚠️ Educational use only. Run in a **sandbox/VPS** you can reset. Do **NOT** run on production machines.

## 🚀 Quick Start
```bash
python honeypot.py
# (Optional) edit ports/banners in config.json first
```
Let it run. When attacks or scans happen, events will be written to `logs/alerts.jsonl`.

## 📊 Visualize Attacks
Open `web/index.html` in your browser and **upload** the `logs/alerts.jsonl` file. You'll see:
- Events by Type
- Top Source IPs
- Ports Targeted
- Recent Events

*(Everything is processed locally in your browser — no backend required.)*

## 🔧 Configure
Edit `config.json`:
```json
{
  "ports": [22,23,80],
  "banners": {
    "22": "SSH-2.0-OpenSSH_7.4",
    "23": "Welcome to BusyBox v1.31.1 (built-in shell)\nlogin: ",
    "80": "HTTP/1.1 200 OK\r\nServer: Apache\r\n\r\n"
  }
}
```

## 📂 Structure
```
HoneyWatch/
  honeypot.py
  analyze.py
  modules/
    logger.py
  logs/
    alerts.log
    alerts.jsonl
  web/
    index.html
  config.json
  README.md
```

## 🛡️ Notes
- Low‑interaction by design (safe). We log and pretend, we never execute payloads.
- For more realism, deploy on a cloud VPS with open security‑group ports.
- Add geo‑IP enrichment later by pre‑processing `alerts.jsonl` with a script.

---

**Built for learning & portfolio impact.** PRs welcome.
