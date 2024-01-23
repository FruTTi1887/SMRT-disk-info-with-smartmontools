import re
from contextlib import redirect_stdout
from pySMART import Device
import pySMART
import shutil
import requests
import os
import psutil
from itertools import zip_longest
import subprocess
TOKEN = "6228036250:AAG0ZyujGTT9nGcO7RP0oVRD2V8uWNdZcuk"
chat_id = "6004481260"


f = open('D:/TT/start_sklad.bat', 'r')
lines = f.readlines()[1:2]
for line in lines:
    ttname = line[147:-6]


try:
    # копирование библиотеки smartmontools
    shutil.copytree('D:/TT/smartmontools', 'C:/Program Files/smartmontools')
except:
    True

try:
    shutil.copyfile('D:/TT/log.txt',
                    'D:/TT/logout.txt')
except:
    True
device = pySMART.Device('/dev/sda')
sda = Device('/dev/sda')
needsword = ['Hours', 'Reallocated']


with open('D:/TT/Temp.txt', 'w') as f:  # создание файла Temp.txt со всеми аттрибутами
    with redirect_stdout(f):
        sda.all_attributes()


f = open('D:/TT/Temp.txt', 'r')
lines = f.readlines()
log = open('D:/TT/log.txt', 'w')
for line in lines:
    if needsword[0] in line or needsword[1] in line:
        log.write(line)
log.close()


with open("D:/TT/Temp.txt", "r") as file:  # Получение температуры диска
    text = file.readlines()
for line in text:
    if 'Temperature' in line:
        pattern = r'\d+'
        result = re.findall(pattern, line)
Temperature = int(result[4])


if Temperature > 70:
    message = "Alarm " + ttname + " Температура больше 70!"
    url = f"https://api.telegram.org/bot{
        TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()


try:
    with open('D:/TT/log.txt') as first_file, open('D:/TT/logout.txt') as second_file:
        for first_line, second_line in zip_longest(first_file, second_file):
            if 'Hours' in first_line:
                continue
            if first_line != second_line:
                message = "Alarm " + ttname
                url = f"https://api.telegram.org/bot{
                    TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url).json()
                break
except:
    True
