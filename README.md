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

### Option 1: Download Pre-compiled Agent
Download the ready-to-use Windows executable:
**[Download agent_main.exe](https://github.com/PrabhatTheCoder/Process-Monitoring/blob/main/agent_main.exe)**

### Option 2: Compile from Source
1. Navigate to the `agent/` directory
2. Compile the agent to EXE:
   ```bash
   pyinstaller --onefile agent.py
   ```

### Running the Agent
1. Run `agent_main.exe` on your Windows system:
   ```cmd
   agent_main.exe --server ws://<server-ip>:8000/ws/monitor/<hostname>/
   ```
   
2. **Example usage:**
   ```cmd
   agent_main.exe --server ws://52.66.248.191:8000/ws/monitor/your-hostname/
   ```

The agent will start streaming real-time process data from your Windows machine to the Django backend.

> **Note:** `agent_main.exe` is specifically designed to fetch processing data from Windows systems and stream it to the monitoring dashboard in real-time.

---

## 📷 Screenshots

### Live Process Dashboard
![Process Monitoring Dashboard](http://52.66.248.191:8000/)

---

## 📌 To-Do

- [ ] Add authentication for WebSocket connections
- [ ] Export process logs to CSV/JSON  
- [ ] Support Linux & Mac agents
- [ ] Add alerts for high CPU/memory usage
- [ ] Process filtering and search functionality
- [ ] Historical data visualization charts

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
