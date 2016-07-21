import paramiko
import subprocess, sys
import time
import random

#Clear exit on Ctrl+C
def ctrl_c_exeption(type, value, tb):
    if not issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
if sys.stdin.isatty():
    sys.excepthook = ctrl_c_exeption

#Declaring open ports
open_ports = {'50000',
              '50001',
              '50010',
              '50011',
              '50012',
              '13400',
              '445',
              '53',
              '53'}

send_data = ["*^*R2D2\n", "*^*42\n"]

#open ssh connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy()
)
ssh.connect('198.18.34.1',
            username='root',
            password='root')

#parameters
target_ip = "198.18.34.1"
udp_param = "-u"
listen_param = "-l"
nc_ = "nc"

def test_fail(nc):
    print "\nTEST FAILED"
    ssh.close()
    nc.kill()
    sys.exit()

#nonblocking netcat reading
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

def processing(shell, nc):
    # send from laptop to target
    for d in range(len(send_data)):
        nc.stdin.write(send_data[d])
        time.sleep(0.3)
        try:
            reply = shell.recv(2024)
        except Exception:
            continue
        str = send_data[d]
        str = str[:-1]
        if str in reply:
            test_fail(nc)

    # send from target to laptop
    for d in range(len(send_data)):
        shell.send(send_data[d])
        time.sleep(0.3)
        reply = " "
        try:
            reply = read(nc.stdout.fileno(), 1024)
        except OSError:
            continue
        str = send_data[d]
        str = str[:-1]
        if str in reply:
            test_fail(nc)

def netcating(ssh_nc, sub_nc):
    shell = ssh.invoke_shell()
    shell.settimeout(1)
    shell.recv(2024)
    shell.send(ssh_nc)
    shell.recv(2024)

    time.sleep(1)

    nc = subprocess.Popen(sub_nc,
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    flags = fcntl(nc.stdout, F_GETFL)
    fcntl(nc.stdout, F_SETFL, flags | O_NONBLOCK)

    processing(shell, nc)
    nc.kill()
    shell.close()


#test all ports
for i in range(100):
    #exec ssh command & subprocess
    p = random.randrange(0, 60000, 100)
    port = str(p)
    if port in open_ports:
        continue

    print "........processing........."

    #run for tcp protocol
    cmd_ssh = nc_ + " " + listen_param + " "+ port + '\n'
    cmd_nc = [nc_, target_ip, port]

    netcating(cmd_ssh, cmd_nc)

    #run for udp protocol
    cmd_ssh = nc_ + ' -v ' + udp_param + " " + listen_param + " " +  port +"\n"
    cmd_nc = [nc_, udp_param, target_ip, port]

    netcating(cmd_ssh, cmd_nc)

print "\nTEST PASSED"
sys.exit()