# build.sh (ตรวจสอบว่ามีไฟล์นี้อยู่ในโปรเจกต์)

#!/usr/bin/env bash

# Exit on error
set -o errexit

# ติดตั้ง Dependencies
pip install -r requirements.txt

# รวบรวม Static Files (CSS, JS, Images)
python manage.py collectstatic --no-input

# อัปเดตโครงสร้างฐานข้อมูล
python manage.py migrate