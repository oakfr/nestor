#!/usr/bin/env python
from transport import BusChecker
import Tkinter as tk
import time
import functools



def Draw(root, bus_checker):
    """ draw function.  is called only once at startup. """

    # create the main frame
    frame=tk.Frame(root,width=1000,height=500,relief='solid',bd=0,bg='white')
    frame.pack()

    # select font

    # create the graphical objects
    label_lines_names = []
    label_lines_times = []
    n_lines = len(bus_checker.lines_names_sorted())
    for v in bus_checker.lines_names_sorted():
        mfont = ("TkFixedFont",12)
        mfont = ("-*-lucidatypewriter-medium-r-*-*-*-140-*-*-*-*-*-*",12)
        mfont = ("FixedSys", 24)
        label1 = tk.Label(frame,text=v.rjust(10),font=mfont)
        label2 = tk.Label(frame,text='',font=mfont)
        label1.config(bg='white',justify='right')
        label2.config(bg='white',justify='left')
        label_lines_names.append(label1)
        label_lines_times.append(label2)

    # place objects on a grid
    for (label1,label2,k) in zip(label_lines_names,label_lines_times,range(n_lines)):
        print('setting label %d' % k)
        label1.grid(row=k)
        label2.grid(row=k,column=1)

    return label_lines_times


def Refresher(root, bus_checker, label_lines_times):
    """ refresh function. is called repeatedly. """

    print('refreshing at %s...' % time.asctime())
    bus_checker.refresh()
    times_sorted = bus_checker.lines_times_sorted()

    # update text for each bus line
    for v,k in zip(times_sorted, range(len(times_sorted))):
        vt = ', '.join(['%d' % x for x in v])
        if len(v) > 0:
            vt += ' mn'
        else:
            vt = ''
        vt = ' ' + vt.ljust(25)
        print(vt)
        label_lines_times[k].configure(text=vt)

    # call itself
    root.after(1000, functools.partial(Refresher,root,bus_checker,label_lines_times)) # every second...
    #root.geometry("500x500")


def main():
    bus_checker = BusChecker()
    bus_checker.refresh()

    root = tk.Tk()
    lines_next = Draw(root, bus_checker)
    Refresher(root, bus_checker, lines_next)
    root.mainloop()


if __name__ == "__main__":
    main()
