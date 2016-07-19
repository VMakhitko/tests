import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy()
)
ssh.connect('198.18.34.1', username='root',
            password='root')

stdin, stdout, stderr = ssh.exec_command("ls -la /")

type(stdin)

print stdout.readlines()
