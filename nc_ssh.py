import subprocess, time

nc = subprocess.Popen(["nc", "198.18.34.1", "13400"],
                      stdin=subprocess.PIPE,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)



while True:
    print nc.stdin.write('qweerrt\n')
    time.sleep(1)