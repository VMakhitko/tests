import paramiko
import subprocess, sys
import time

#Clear exit on Ctrl+C
def ctrl_c_exeption(type, value, tb):
    if not issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
if sys.stdin.isatty():
    sys.excepthook = ctrl_c_exeption

#Declaring services ports and protocol types
services = [['50000', 'u'],
            ['50001', 'u'],
            ['50010', 'u'],
            ['50011', 'u'],
            ['50012', 'u'],
            ['13400', ''], #empty second parameter mean tcp protocol type
            ['445', ''],
            ['53', 'u'],
            ['53', '']]

send_data = ["*^*open\n",
        "*^*close\n",
        "*^*back\n",
        "*^*forward\n",
        "*^*left\n",
        "*^*right\n",
        "*^*wrong\n",
        "*^*R2D2\n",
        "*^*42\n"]

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
nc_obd = "nc.netcat-openbsd "

def test_fail(nc):
    print "\nTEST FAILED"
    ssh.close()
    nc.kill()
    sys.exit()

def processing(shell, nc):
    # send from laptop to target
    for d in range(len(send_data)):
        nc.stdin.write(send_data[d])
        time.sleep(0.3)
        reply = shell.recv(2024)
        str = send_data[d]
        str = str[:-1]
        if str not in reply:
            test_fail(nc)

    # send from target to laptop
    for d in range(len(send_data)):
        shell.send(send_data[d])
        time.sleep(0.3)
        reply = nc.stdout.readline()
        str = send_data[d]
        str = str[:-1]
        if str not in reply:
            test_fail(nc)

def netcating(ssh_nc, s_nc):
    shell = ssh.invoke_shell()
    shell.send(ssh_nc)
    shell.recv(2024)

    time.sleep(1)

    nc = subprocess.Popen(s_nc,
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    processing(shell, nc)
    shell.close()
    nc.kill()

#test all ports
for i in range(len(services)):
    print "........processing.........."
    #exec ssh command & subprocess
    if not services[i][1]:
        cmd_ssh = nc_ + " " + listen_param + " "+ services[i][0] + '\n'
        cmd_sub = [nc_, target_ip, services[i][0]]

        netcating(cmd_ssh, cmd_sub)

    else:
        cmd_ssh = nc_ + " -v " + udp_param + " " + listen_param + " " +  services[i][0] +"\n"
        cmd_sub = [nc_, udp_param, target_ip, services[i][0]]

        netcating(cmd_ssh, cmd_sub)

print "TEST PASSED"
sys.exit()

