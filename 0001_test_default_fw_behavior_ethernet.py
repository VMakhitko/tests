
#This is a test for iptables default rules
#
#Set following rules on target
#iptables -P INPUT DROP
#iptables -P FORWARD DROP
#iptables -P OUTPUT DROP

#Run this script on host
#Any data shouldn't goes through

#Use nc.netcat-openbsd for setup netcat connection
#Recipe: meta-networking/recipes-support/netcat/netcat-openbsd_1.105.bb

import time
import serial
import sys
import subprocess

#Clear exit on Ctrl+C
def ctrl_c_exeption(type, value, tb):
    if not issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
if sys.stdin.isatty():
    sys.excepthook = ctrl_c_exeption

#Setup serial console
serial_device = "/dev/ttyUSB0"
serial_command = "nc.netcat-openbsd -l 50000\n"

nc_command = "nc 198.18.34.1 50000"

serial = serial.Serial(serial_device, baudrate=115200)
serial.write(serial_command)

time.sleep(0.5)

nc_process = subprocess.Popen(nc_command, shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE)

time.sleep(0.5)

test_text = ["open\n", "close\n", "back\n", "forward\n",
            "left\n", "right\n", "wrong\n", "R2D2\n", "42\n"]

from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

flags = fcntl(nc_process.stdout, F_GETFL)
fcntl(nc_process.stdout, F_SETFL, flags | O_NONBLOCK)

test_status = True

for t in test_text:
    serial.write(t)
    time.sleep(0.2)
    try:
        print read(nc_process.stdout.fileno(), 1024)
    except OSError:
        print 'No data'
        test_status = True
        continue
    test_status = False
    break

if test_status:
    print 'TEST PASS'
else:
    print 'TEST FAILED'

#Clear
nc_process.kill()
serial.write('\x03')
serial.close()
