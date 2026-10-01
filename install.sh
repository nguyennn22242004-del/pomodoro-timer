#!/bin/bash

echo "=== Cài đặt ứng dụng Pomodoro Timer trên Ubuntu ==="

# Cập nhật danh sách gói dịch vụ
sudo apt update

# Cài đặt Python3, pip và các thư viện cần thiết
sudo apt install -y python3 python3-pip python3-pyqt6

# Cấp quyền thực thi cho các file script
chmod +x pomodoro.sh
chmod +x install.sh

echo "=== Cài đặt hoàn tất! Thử khởi chạy ứng dụng bằng cách gõ: ./pomodoro.sh ==="
