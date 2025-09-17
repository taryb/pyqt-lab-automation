# Lab Automation Demo (PyQt5)

Simple demo app built with PyQt5 to simulate lab automation workflows.
⚠️ Note: This demo pins `numpy<2` to avoid ABI issues with optional dependencies like `bottleneck`.

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/app.py
