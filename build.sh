#!/bin/bash
set -e

echo "=== Checking Python version ==="
python3 --version

echo "=== Upgrading pip, setuptools, and wheel ==="
python3 -m pip install --upgrade pip setuptools wheel

echo "=== Installing requirements ==="
python3 -m pip install -r requirements.txt

echo "=== Build complete ==="

