import asyncio
import json
import os
from datetime import datetime
from modules.logger import Reporter

BANNERS = {
    22: "SSH-2.0-OpenSSH_7.4\r\n",
    23: "Welcome to BusyBox v1.31.1 (built-in shell)\r\nlogin: ",
    80: "HTTP/1.1 200 OK\r\nServer: Apache/2.4.29\r\nContent-Length: 0\r\n\r\n",
    443: ""
}

class HoneyWatchServer(asyncio.Protocol):
    def __init__(self, port, reporter, banner=""):
        self.port = port
        self.reporter = reporter
        self.banner = banner.encode() if banner else b""
        self.transport = None
        self.peer = None

    def connection_made(self, transport):
        self.transport = transport
        try:
            self.peer = transport.get_extra_info('peername')
        except Exception:
            self.peer = None
        if self.banner:
            try:
                self.transport.write(self.banner)
            except Exception:
                pass
        ip = self.peer[0] if self.peer else "unknown"
        self.reporter.alert("connection", f"Connection on port {self.port} from {ip}", {"ip": ip, "port": self.port})

    def data_received(self, data):
        text = data[:200].decode(errors='ignore')
        ip = self.peer[0] if self.peer else "unknown"
        self.reporter.alert("payload", f"Data on port {self.port} from {ip}: {text!r}", {"ip": ip, "port": self.port, "data": text})

    def connection_lost(self, exc):
        ip = self.peer[0] if self.peer else "unknown"
        self.reporter.alert("disconnect", f"Disconnect on port {self.port} from {ip}", {"ip": ip, "port": self.port})

async def run_servers(ports, reporter, banners):
    loop = asyncio.get_running_loop()
    servers = []
    for p in ports:
        banner = banners.get(p, "")
        server = await loop.create_server(lambda: HoneyWatchServer(p, reporter, banner), "0.0.0.0", p)
        servers.append(server)
        print(f"🟢 Listening on 0.0.0.0:{p}")
    try:
        await asyncio.gather(*(s.serve_forever() for s in servers))
    finally:
        for s in servers:
            s.close()
            await s.wait_closed()

def load_config(path="config.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            cfg = json.load(f)
        # convert string keys to int for banners if needed
        banners = cfg.get("banners", {})
        cfg["banners"] = {int(k): v for k, v in banners.items()} if banners else {}
        return cfg
    return {"ports": [22, 23, 80], "banners": BANNERS}

def main():
    cfg = load_config()
    ports = cfg.get("ports", [22, 23, 80])
    banners = cfg.get("banners", BANNERS)
    reporter = Reporter(log_path="logs/alerts.log", json_path="logs/alerts.jsonl")
    print("🚧 HoneyWatch starting... Press Ctrl+C to stop.")
    try:
        asyncio.run(run_servers(ports, reporter, banners))
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")

if __name__ == "__main__":
    main()
