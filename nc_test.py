#!/usr/bin/python

import subprocess
import select
import sys, time

proc_2 = subprocess.Popen(["nc", "-l", "2001"],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)

#time.sleep(0.1)

proc = subprocess.Popen(["nc", "localhost", "2001"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)


i = 0
while True:
    i += 1
    print "Iteration: " + str(i)
    proc_2.stdin.write("proc_2\n")
    time.sleep(0.5)
    print "proc Try read: " +  proc.stdout.readline()
    time.sleep(0.5)
    proc.stdin.write("proc\n")
    time.sleep(0.5)
    print "proc_2 try read: " + proc_2.stdout.readline()

#outfile = proc.stdout
#outfd = outfile.fileno()

#infile = proc.stdin
#infd = infile.fileno()

#p = select.poll()
#p.register(outfd, select.POLLIN)
#p.register(sys.stdin.fileno(), select.POLLIN);

#while True:
#    ready = p.poll()

#    try:
#        e = ready.pop()
#    except IndexError:
#        continue

#    fd, ev = e

#    if fd == 0:
#        t = sys.stdin.readline()
#        infile.write(t)

#    if fd == outfd:
#        t = outfile.readline()
#        if t:
#            print t