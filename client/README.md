# 🚀 Real-time Server Monitor Dashboard

A full-stack application that monitors and visualizes system performance (CPU, RAM, and Disk Usage) in real-time. The system consists of a Python agent gathering metrics, a Flask API processing the data, and a React frontend visualizing the trends.

![Demo Preview](demo.gif) 
## 🛠 Tech Stack
* **Frontend:** React (Vite), Recharts, Axios
* **Backend:** Python, Flask, Flask-CORS
* **Agent:** Python, Psutil
* **Architecture:** REST API, Polling

## 🌟 Features
* **Real-time Data Collection:** A Python agent runs locally to harvest system metrics every 10 seconds.
* **Live Visualization:** Interactive graphs showing historical trends for CPU, RAM, and Disk usage.
* **Robust Error Handling:** Handles server downtime and network issues gracefully.

## 🚀 How to Run Locally

1. Start the Server (Backend)
Navigate to the server directory and start the Flask app:
```bash
cd server
pip install flask flask-cors
python app.py

2. Start the Dashboard (Frontend)
Open a new terminal, navigate to the client, and start React:
cd client
npm install
npm run dev

3. Start the Agent
Open a third terminal and run the monitoring agent:
cd agent
pip install psutil requests
python agent.py