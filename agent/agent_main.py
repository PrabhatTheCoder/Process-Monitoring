import asyncio
import json
import websockets
import platform
import psutil
from datetime import datetime, timezone
import socket
import os

WS_SERVER_URL = "ws://52.66.248.191:8000/ws/process/"
SEND_INTERVAL = 5
SNAPSHOT_FLAG_FILE = "snapshot_sent.flag"

# Collect system info (snapshot)

def get_system_info():
    vm = psutil.virtual_memory()
    du = psutil.disk_usage('/')

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "processor": platform.processor(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "total_ram": round(vm.total / (1024 * 1024), 2),
        "available_ram": round(vm.available / (1024 * 1024), 2),
        "used_ram": round(vm.used / (1024 * 1024), 2),
        "total_storage": round(du.total / (1024 * 1024 * 1024), 2),
        "used_storage": round(du.used / (1024 * 1024 * 1024), 2),
        "available_storage": round(du.free / (1024 * 1024 * 1024), 2),
    }


# Collect process info
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            processes.append({
                "pid": info['pid'],
                "parent_pid": info['ppid'],
                "name": info['name'],
                "cpu_usage": info['cpu_percent'],
                "memory_usage": info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

async def send_data():
    async with websockets.connect(WS_SERVER_URL) as ws:
        print("Connected to WebSocket server...")

        hostname = socket.gethostname()

        # Send system snapshot only once
        if not os.path.exists(SNAPSHOT_FLAG_FILE):
            print("Sending system snapshot...")
            system_info = get_system_info()
            processes = get_processes()
            payload = {
                "system_info": system_info,
                "processes": processes
            }
            await ws.send(json.dumps(payload))
            with open(SNAPSHOT_FLAG_FILE, "w") as f:
                f.write("sent")
        else:
            print("Snapshot already sent. Skipping...")

        # Now send only process updates every 5s
        while True:
            print(f"Sending process stream at {datetime.now(timezone.utc).isoformat()}")
            payload = {
                "system_info": get_system_info(),  # still needed per server logic
                "processes": get_processes()
            }
            await ws.send(json.dumps(payload))
            await asyncio.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    asyncio.run(send_data())
