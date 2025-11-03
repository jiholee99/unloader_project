# Unloader Project

A Python-based GUI application (PySide6) for roller image processing and distance validation.

---

## Requirements
- Python 3.10 or higher
- pip (Python package manager)

---


## Project Enviornment Setup (Rasberry PI)
```bash
python -m venv .venv
source .venv/bin/activate     # On Linux/macOS
.venv\Scripts\activate        # On Windows
pip install -r requirements.txt
sudo apt update
sudo apt install python3-pyqt5
```

# Important Notes
- Right now test app with main.py.
- Have to refactor all the UI code to run on ARM architecture on linux (PyQt6 doesn't support linux)
