# Unloader Project

A Python-based GUI application (PySide6) for roller image processing and distance validation.
Inspection is designed to work on any system. (Might have to tweak what gets passed into inspection service)
Inspection is being worked on to implment other inspection in the future.
---

# Service Overview
- Service below are created to be independent and flexible
- ![Service overview](Service_Overview.png)

## Requirements
- python version specified in .python-version
- uv
- picamera2
---


## Project Enviornment Setup (Rasberry PI)
```bash
pip install uv
- After installing uv,
uv sync
```

## To Run the project
### Main CLI of the app
```bash
uv python -m main
```
### GUI Debugger
```bash
uv python -m ui.main
```

# Important Notes
- Right now test app with main.py.
