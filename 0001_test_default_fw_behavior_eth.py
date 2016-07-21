import time
import serial
import sys
import subprocess

from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

#Clear exit on Ctrl+C
def ctrl_c_exeption(type, value, tb):
    if not issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
if sys.stdin.isatty():
    sys.excepthook = ctrl_c_exeption

#Setup serial console
serial_device = "/dev/ttyUSB0"
serial_command = "nc.netcat-openbsd -l 40000\n"

nc_command = "nc 198.18.34.1 40000"

test_text = ["*^*open\n",
             "*^*close\n",
             "*^*back\n",
             "*^*forward\n",
             "*^*left\n",
             "*^*right\n",
             "*^*wrong\n",
             "*^*R2D2\n",
             "*^*42\n"]

sport = None
nc_process = None

def init():
    try:
        s = serial.Serial(serial_device, baudrate=115200, timeout=1)
        s.readlines() #move pointer
        s.write(serial_command)
    except serial.SerialException:
        print "SerialException: try sudo..."
        sys.exit()

    time.sleep(0.5)

    nc = subprocess.Popen(nc_command, shell=True,
                                  stdout=subprocess.PIPE,
                                  stdin=subprocess.PIPE)

    time.sleep(0.5)

    flags = fcntl(nc.stdout, F_GETFL)
    fcntl(nc.stdout, F_SETFL, flags | O_NONBLOCK)
    return s, nc

def close(sport, nc_process):
    nc_process.kill()
    sport.write('\x03')
    sport.close()

test_status = True

sport, nc_process = init()
for t in test_text:
    sport.write(t)
    time.sleep(0.2)
    try:
        read(nc_process.stdout.fileno(), 1024)
    except OSError:
        test_status = True
        continue
    test_status = False
    break
close(sport, nc_process)

sport, nc_process = init()
for t in test_text:
    nc_process.stdin.write(t)
    time.sleep(1)
    reply =  sport.readline()
    str = t[:-1]
    if str in reply:
        test_status = False
        break
close(sport, nc_process)

if test_status:
    print 'TEST PASS'
else:
    print 'TEST FAILED'

