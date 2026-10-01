#!/bin/bash
# Script chạy ứng dụng Pomodoro Timer trên Ubuntu

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python3 "$SCRIPT_DIR/pomodoro_linux/app.py"
