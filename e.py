from __future__ import print_function
import sys
from itertools import cycle
from subprocess import Popen, PIPE
from textwrap import dedent

# start child process
p = Popen([sys.executable or 'python', '-u', '-c', dedent("""
        for i in range(10):
            x = int(input('Enter x-dimension: '))
            print(x*x)
        """)], stdin=PIPE, stdout=PIPE, universal_newlines=True, bufsize=1)
for n in cycle([3, 1, 4, 15, 926]): # infinite loop
    while p.poll() is None: # while the subprocess is running
        # send input to the child
        print(n, file=p.stdin)
        # read & parse answer
        data = p.stdout.readline().rpartition(' ')[2]
        if not data: # EOF
            answer = None
            break # exit inner loop
        answer = int(data)
        if answer == 1: # show example when input depends on output
            n += 1
        else: # done with given `n`
            break # exit inner loop
    else: # subprocess ended
        break # exit outer loop
    if answer is not None:
        print("Input %3d Output %6d" % (n, answer))
p.communicate() # close pipes, wait for the child to terminate