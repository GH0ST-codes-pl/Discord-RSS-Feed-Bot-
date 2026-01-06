#!/bin/bash
# Automatyczne uruchamianie bota Discord

cd "$(dirname "$0")" || exit 1
./venv/bin/python bot.py
