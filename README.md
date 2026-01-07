# Naukri Automation Scripts

Simple collection of scripts to automate Naukri login and uploads.

Prerequisites
- Python 3.8+ and a virtual environment
- Install dependencies if a `requirements.txt` exists

Quick setup (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Usage
- Save or refresh login/cookie files:

```powershell
python save_naukri_login.py
python save_naukri_cookies.py
```

- Run upload script (example):

```powershell
python naukri_playwright_upload.py
```
