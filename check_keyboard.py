import time
import uinput
from subprocess import Popen, PIPE
import os

def keypress():
    device = uinput.Device([uinput.KEY_A])
    device.emit_click(uinput.KEY_E)

def keypress2 ():
    sequence = "key S"
    #p = Popen(['xte'], stdin=PIPE)
    #p.communicate(input=sequence)
    #os.cmd ('xte \'key s\'')
    os.system('xte \'key S\'')

def main():
    for i in range(1000):
        print('hey!')
        time.sleep(1)
        keypress2()


if __name__ == "__main__":
    main()

