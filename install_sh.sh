#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Installation done. Run: source venv/bin/activate && python cli_chat.py"
