import paramiko
import subprocess, sys
import time
import random

#Declaring open ports
open_ports = {'50001',
              '50001',
              '50010',
              '50011',
              '50012',
              '13400',
              '445',
              '53',
              '53'}

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
nc = ""


#parameters
target_ip = "198.18.34.1"
udp_param = "-u"
listen_param = "-l"
nc_ = "nc"
nc_obd = "nc.netcat-openbsd "
test_status = True

def processing(shell, nc):
    # send from laptop to target
    for d in range(len(send_data)):
        # shell.send(send_data[d])
        nc.stdin.write(send_data[d])
        time.sleep(0.3)
        reply = shell.recv(2024)
        #print "ssh read: " + reply
        str = send_data[d]
        str = str[:-1]
        if str not in reply:
            print "TEST FAILED"
            sys.exit()

    # send from target to laptop
    for d in range(len(send_data)):
        shell.send(send_data[d])
        # nc.stdin.write(send_data[d])
        time.sleep(0.3)
        # reply = shell.recv(2024)
        reply = nc.stdout.readline()
        #print "nc read: " + reply
        str = send_data[d]
        str = str[:-1]
        if str not in reply:
            print "TEST FAILED"
            sys.exit()


#test all ports
for i in range(1000):
    #exec ssh command & subprocess
    p = random.randrange(0, 60000, 100)
    port = str(p)
    print "Random port: " + port

    #run for tcp protocol
    print "Debug: " + nc_ + listen_param + port
    shell = ssh.invoke_shell()
    print shell.recv(2024)
    cmd = nc_ + " " + listen_param + " "+ port + '\n'
    print "cmd: " + cmd
    shell.send(cmd)
    print "nc " + shell.recv(2024)

    time.sleep(1)

    print "Debug subproc: " + nc_ + " " + target_ip + " " + port
    nc = subprocess.Popen([nc_, target_ip, port],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    time.sleep(0.1)
    processing(shell, nc)
    nc.kill()
    shell.close()

    #run for udp port
    shell = ssh.invoke_shell()
    cmd = nc_ + ' -v ' + udp_param + " " + listen_param + " " +  port +"\n"
    shell.send(cmd)
    shell.recv(2024)

    time.sleep(1)

    print "Debug subproc: " + nc_ + udp_param + target_ip + port
    cmd = [nc_, udp_param, target_ip, port]

    nc = subprocess.Popen([nc_, udp_param, target_ip, port],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    time.sleep(0.1)
    processing(shell, nc)
    nc.kill()
    shell.close()

print "TEST PASSED"
sys.exit()