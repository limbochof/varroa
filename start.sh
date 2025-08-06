#!/bin/bash
python -m pip install --upgrade pip setuptools wheel
pip install --no-build-isolation aiogram==3.4.1
pip install --no-build-isolation -r requirements.txt
python bot.py
