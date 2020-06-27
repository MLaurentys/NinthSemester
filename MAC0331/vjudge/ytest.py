import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import signal
import numpy as np

def gen(ind):
    if os.path.isfile('tst' + str(ind)):
        os.remove('tst'+str(ind))
    randPoints = np.random.rand(5000000, 2) * 1000000
    print('tst' + str(ind))
    f = open("tst" + str(ind), 'w')
    f.write(str(len(randPoints)) + '\n')
    for pt in randPoints:
        f.write(str(pt[0]) + ' ' + str(pt[1]) + '\n')
    f.write('0')
    f.close()

def main():
    for j in range(1):
        for i in range(1):
            if os.path.isfile('o' + str(i)):
                os.remove('o'+str(i))
            gen(i)
            inp = open('tst' + str(i))
            out = open('o' + str(i), 'w')
            proc = subprocess.Popen(["./a.out"], stdin=inp, stdout=out)

            proc.wait()
            if proc.returncode == -signal.SIGSEGV:
                print("ERRO")
                break
            inp.close()
            out.close()

if __name__=='__main__':
    main()