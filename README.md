# 🖥️ Process Monitoring System

A **real-time process monitoring system** built with **Python, Django, and WebSockets**.  
It collects process and system metrics from a lightweight **Windows Agent (`agent_main.exe`)**, streams them to a Django backend, and displays the process hierarchy with CPU/memory usage on a live dashboard.  

**Live Demo:** [http://52.66.248.191:8000/](http://52.66.248.191:8000/)

---

## 🚀 Features

- 📡 **Real-time streaming** of process data using **WebSockets**  
- 🖥️ **Windows Agent (`agent_main.exe`)** for process & system metric collection  
- 📊 **Frontend dashboard** for process hierarchy visualization  
- 🧩 Displays:
  - Process name & PID
  - CPU usage
  - Memory usage
  - Parent/child process structure
- 🗄 **Historical system snapshots** stored for analysis  
- 🔍 Filter processes by hostname  
- 🛠 Easy deployment with **Docker**

---

## 🛠 Tech Stack

- **Backend:** Django, Django REST Framework, Django Channels (WebSockets)
- **Frontend:** HTML, CSS, JavaScript (Bootstrap)
- **Agent:** Python (compiled to EXE with PyInstaller)
- **Database:** SQLite (default) – can be switched to PostgreSQL
- **Cloud Hosting:** AWS EC2
- **Deployment:** Docker & Docker Compose

---

## 📂 Project Structure

```
Process-Monitoring/
│
├── agent/                    # Windows agent source code
├── agent_main.exe           # Compiled Windows agent executable
├── app/                     # Django app for API & WebSocket handling
├── templates/               # HTML templates for frontend
├── static/                  # Static assets (CSS, JS)
├── manage.py
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/PrabhatTheCoder/Process-Monitoring.git
cd Process-Monitoring
```

### 2️⃣ Run with Docker
```bash
docker-compose up --build
```
This will start:
- Django backend
- WebSocket server
- SQLite database

### 3️⃣ Access the dashboard
```
http://localhost:8000
```

---

## 🌐 API Endpoints

**Base URL:** `http://52.66.248.191:8000/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/available-host/` | GET | Returns a list of all available hosts |
| `/api/system-snapshot/?host_id=<UUID>` | GET | Returns system snapshots for a given host |

### Example Response – `/api/available-host/`

```json
[
    {
        "id": "b4384b78-4737-4020-8280-cf9e7b41f651",
        "name": "prabhat-Nitro-AN515-57",
        "created_at": "2025-08-08T06:02:02.624261Z"
    }
]
```

### Example Response – `/api/system-snapshot/?host_id=...`

```json
[
    {
        "id": "cabe7ddd-e58e-4112-9f9b-bff4bff2fcfe",
        "hostname": "prabhat-Nitro-AN515-57",
        "os": "Linux",
        "processor": "x86_64",
        "cpu_cores": 8,
        "threads": 16,
        "total_ram": 15768.29,
        "available_ram": 4527.27,
        "used_ram": 9756.61,
        "total_storage": 71.18,
        "used_storage": 65.53,
        "available_storage": 2.25,
        "created_at": "2025-08-08T08:18:17.002933Z",
        "host": "b4384b78-4737-4020-8280-cf9e7b41f651"
    }
]
```

---

## 🔌 WebSocket – Live Process Data

**Endpoint:**
```
ws://<server-ip>:8000/ws/monitor/<hostname>/
```

**Example:**
```
ws://52.66.248.191:8000/ws/monitor/prabhat-Nitro-AN515-57/
```

Returns a continuous JSON stream of running processes with:
- Process name
- PID
- CPU usage
- Memory usage
- Parent PID (PPID)

---

## 📡 Windows Agent Setup

### 🚀 Quick Start (Recommended)
**Simply download and run the Windows executable - it will automatically fetch data and send it to the server!**

**[📥 Download agent_main.exe](https://github.com/PrabhatTheCoder/Process-Monitoring/raw/main/agent_main.exe)**

### How to Use:
1. **Download** the `agent_main.exe` file from the link above
2. **Double-click** the executable on your Windows machine
3. **Windows Defender Warning:** You may see a Windows Defender SmartScreen warning:
   - Click **"More info"**
   - Then click **"Run anyway"**
   - This is normal for unsigned executables and the software is safe to run
4. **That's it!** The agent will automatically:
   - Start collecting process data from your system
   - Connect to the server at `ws://52.66.248.191:8000`
   - Begin streaming real-time data to the dashboard
5. **View your data** on the live dashboard: [http://52.66.248.191:8000/](http://52.66.248.191:8000/)

> **✨ Note:** The agent runs automatically once clicked - no command-line setup required! It will instantly start fetching processing data from your Windows system and streaming it to the monitoring dashboard.

> **🛡️ Security Notice:** Windows Defender may show a warning because the executable is not digitally signed. The software is completely safe - just click "More info" → "Run anyway" to proceed.

### Advanced Usage (Custom Server)
If you want to connect to a different server:
```cmd
agent_main.exe --server ws://<your-server-ip>:8000/ws/monitor/<hostname>/
```

### Compile from Source (Optional)
1. Navigate to the `agent/` directory
2. Compile the agent to EXE:
   ```bash
   pyinstaller --onefile agent.py
   ```

---

## 📷 Screenshots

### Live Process Dashboard
Visit the dashboard to see real-time process monitoring: **[http://52.66.248.191:8000/](http://52.66.248.191:8000/)**

Once you run `agent_main.exe` on your Windows machine, you'll see your system's processes appear on the dashboard in real-time!

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

**Prabhat Kumar**  
GitHub: [PrabhatTheCoder](https://github.com/PrabhatTheCoder)
