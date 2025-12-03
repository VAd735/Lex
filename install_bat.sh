@echo off
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Installation complete. Run: venv\Scripts\activate && python cli_chat.py
