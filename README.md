# 🛡️ CyberSOC Intrusion Detection Simulator

A simulated Security Operations Center (SOC) project that detects brute-force SSH login attacks using log correlation, timeline tracking, IOC generation, and a full-stack web dashboard.

## 💻 Technologies Used

- Python (Log Correlation & Analysis)
- Flask + Flask-CORS (Backend APIs)
- React.js (Frontend Dashboard)
- Hydra (Attack Simulation)
- SCP (Log Transfer)
- GitHub for Version Control

## 📁 Features

- Detect failed login brute-force attempts
- IOC extraction: attacker IPs, targets
- Timeline visualization of SSH events
- API endpoints for SOC dashboard

## 📦 Project Structure

```bash
CyberSOC-Intrusion-Sim/
├── backend/
├── scripts/
├── logs/
├── reports/
├── templates/
├── visualize_iocs.py
├── users.txt, passwords.txt
