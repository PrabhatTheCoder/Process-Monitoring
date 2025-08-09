Perfect — I’ll update the README.md so it includes your AWS-hosted URL, REST API endpoints, and WebSocket live process feed.

Here’s your improved Markdown README:

markdown
Copy
Edit
# 🖥️ Process Monitoring System

A **real-time process monitoring system** built with **Python, Django, and WebSockets**.  
It collects process and system metrics from a lightweight **Windows Agent (EXE)**, streams them to a Django backend, and displays the process hierarchy with CPU/memory usage on a live dashboard.  

**Live Demo:** [http://52.66.248.191:8000/](http://52.66.248.191:8000/)

---

## 🚀 Features

- 📡 **Real-time streaming** of process data using **WebSockets**  
- 🖥️ **Windows Agent (EXE)** for process & system metric collection  
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

Process-Monitoring/
│
├── agent/ # Windows EXE source code
├── app/ # Django app for API & WebSocket handling
├── templates/ # HTML templates for frontend
├── static/ # Static assets (CSS, JS)
├── manage.py
├── docker-compose.yml
└── README.md

yaml
Copy
Edit

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/PrabhatTheCoder/Process-Monitoring.git
cd Process-Monitoring
2️⃣ Run with Docker
bash
Copy
Edit
docker-compose up --build
This will start:

Django backend

WebSocket server

SQLite database

3️⃣ Access the dashboard
arduino
Copy
Edit
http://localhost:8000
🌐 API Endpoints
Base URL: http://52.66.248.191:8000/

Endpoint	Method	Description
/api/available-host/	GET	Returns a list of all available hosts
/api/system-snapshot/?host_id=<UUID>	GET	Returns system snapshots for a given host

Example Response – /api/available-host/

json
Copy
Edit
[
    {
        "id": "b4384b78-4737-4020-8280-cf9e7b41f651",
        "name": "prabhat-Nitro-AN515-57",
        "created_at": "2025-08-08T06:02:02.624261Z"
    }
]
Example Response – /api/system-snapshot/?host_id=...

json
Copy
Edit
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
🔌 WebSocket – Live Process Data
Endpoint:

php-template
Copy
Edit
ws://<server-ip>:8000/ws/monitor/<hostname>/
Example:

ruby
Copy
Edit
ws://52.66.248.191:8000/ws/monitor/prabhat-Nitro-AN515-57/
Returns a continuous JSON stream of running processes with:

Process name

PID

CPU usage

Memory usage

Parent PID (PPID)

📡 Windows Agent Setup
Navigate to the agent/ directory.

Compile the agent to EXE:

bash
Copy
Edit
pyinstaller --onefile agent.py
Run the EXE on the target Windows system:

bash
Copy
Edit
agent.exe --server ws://<server-ip>:8000/ws/monitor/<hostname>/
The agent will start streaming process data to the backend.

📷 Screenshots
Live Process Dashboard

📌 To-Do
 Add authentication for WebSocket connections

 Export process logs to CSV/JSON

 Support Linux & Mac agents

 Add alerts for high CPU/memory usage

🤝 Contributing
Contributions are welcome!

Fork the repository

Create a feature branch

Submit a pull request

📄 License
This project is licensed under the MIT License.

📬 Contact
Prabhat Kumar
GitHub: PrabhatTheCoder

yaml
Copy
Edit

---

If you want, I can also **add a diagram showing the flow from the Windows Agent → WebSocket → Django Backend → Dashboard** so the README looks visually complete.  
Do you want me to include that?








Ask ChatGPT





ChatGPT can make mistakes. Check important info. See Cookie Preferences.
