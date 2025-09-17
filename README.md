# Lab Automation Demo (PyQt5)

This project is a **simulator** of a 4-camera lab automation system, built with **PyQt5** and **pyqtgraph**.  
It’s not connected to real hardware — the goal is to demonstrate how I design user-friendly tools for data acquisition, visualization, and measurement.

## ✨ What it shows
- Building desktop GUIs with **PyQt5**
- Live streaming 4 simulated cameras in real-time
- Start/Stop controls with adjustable FPS
- "Run Measurement" → averages N frames per camera, computes mean, noise, and SNR
- Progress bar + timestamped log output
- Structured code that can be extended to real devices (e.g., EPICS, scientific cameras)

## 🔮 What I can do beyond this demo
In real lab environments, I have:
- Integrated **EPICS motors and cameras** into custom GUIs
- Automated calibration routines (lateral, Z-axis, background subtraction, FWHM analysis)
- Containerized environments with **Docker** for reproducibility
- Prototyped tools with **LLMs** (LLaMA, Mistral) for research workflows

## 🚀 Quick Start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/app.py


