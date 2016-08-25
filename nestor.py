#!/usr/bin/env python
from transport import BusChecker
from weather import Weather
import Tkinter as tk
import time
import functools
from PIL import ImageTk, Image
#import uinput


def keypress():
    os.system('xte \'key S\'')
    #device = uinput.Device([uinput.KEY_E])
    #device.emit_click(uinput.KEY_E)

def Draw(root, bus_checker, images):
    """ draw function.  is called only once at startup. """

    # create the main frame
    frame=tk.Frame(root,width=500,height=500,relief='solid',bd=0,bg='white')
    frame.pack()

    # select font
    mfont = ("TkFixedFont",12)
    mfont = ("-*-lucidatypewriter-medium-r-*-*-*-140-*-*-*-*-*-*",12)
    mfont = ("FixedSys", 50)

    # create the graphical objects (transport)
    label_lines_names = []
    label_lines_times = []
    label_lines_image = []
    n_lines = len(bus_checker.lines_names_sorted())
    for v in bus_checker.lines_names_sorted():
        label1 = tk.Label(frame,text=v.rjust(10),font=mfont)
        label2 = tk.Label(frame,text='',font=mfont)
        label1.config(bg='white')#,justify='right')
        label2.config(bg='white')#,justify='left')
        label_lines_names.append(label1)
        label_lines_times.append(label2)
        image = tk.Label (frame, image = images[v], borderwidth=0)
        label_lines_image.append(image)
    label_time_of_day = tk.Label(frame,font=mfont)
    label_time_of_day.config(bg='white',justify='right')
    
    # create the graphical objects (weather)
    label_weather_image_morning = tk.Label (frame, image = images['morning'], borderwidth=0)
    label_weather_image_afternoon = tk.Label (frame, image = images['afternoon'], borderwidth=0)
    label_weather_image_evening = tk.Label (frame, image = images['evening'], borderwidth=0)
    label_weather_image_difference = tk.Label (frame, image = images['difference'], borderwidth=0)
    label_weather_image_rain = tk.Label (frame, image = images['umbrella'], borderwidth=0)

    label_weather_text_morning = tk.Label(frame,text='',font=mfont)
    label_weather_text_afternoon = tk.Label(frame,text='',font=mfont)
    label_weather_text_evening = tk.Label(frame,text='',font=mfont)
    label_weather_text_rain = tk.Label(frame,text='',font=mfont)
    label_weather_text_difference = tk.Label(frame,text='',font=mfont)
    
    label_weather_texts = [label_weather_text_morning, label_weather_text_afternoon,\
            label_weather_text_evening, label_weather_text_difference, label_weather_text_rain]
    for label in label_weather_texts:
        label.config(bg='white')

    # place objects on a grid
    label_time_of_day.grid(row=0,columnspan=2)
    for (label1,label2,image,k) in zip(label_lines_names,label_lines_times,label_lines_image,range(n_lines)):
        image.grid(row=k+2,column=0)
        label2.grid(row=k+2,column=1,sticky='W')

    label_weather_image_morning.grid(row=2,column=3)
    label_weather_image_afternoon.grid(row=3,column=3)
    label_weather_image_evening.grid(row=4,column=3)
    label_weather_image_difference.grid(row=5,column=3)
    label_weather_image_rain.grid(row=6,column=3)
    
    label_weather_text_morning.grid(row=2,column=4,sticky='W')
    label_weather_text_afternoon.grid(row=3,column=4,sticky='W')
    label_weather_text_evening.grid(row=4,column=4,sticky='W')
    label_weather_text_difference.grid(row=5,column=4,sticky='W')
    label_weather_text_rain.grid(row=6,column=4,sticky='W')

    objects = (label_time_of_day, label_lines_times, label_weather_texts)

    return objects


def Refresher(root, bus_checker, weather, objects):
    """ refresh function. is called repeatedly. """

    print('refreshing at %s...' % time.asctime())
    
    label_time_of_day = objects[0]
    label_lines_times = objects[1]
    label_weather_texts = objects[2]

    label_time_of_day.configure(text=time.strftime('%A %d %Y    %H:%M'))

    # refresh transportation data
    bus_checker.refresh()
    times_sorted = bus_checker.lines_times_sorted()

    # refresh weather data
    weather.refresh()

    # simulate key press to maintain screen on
    #keypress()

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

    # update text for weather
    degree_sign = u'\N{DEGREE SIGN}'
    label_weather_texts[0].configure(text=(' %d' + degree_sign) % weather.temp_matin)
    label_weather_texts[1].configure(text=(' %d' + degree_sign) % weather.temp_midi)
    label_weather_texts[2].configure(text=(' %d' + degree_sign) % weather.temp_soir)
    label_weather_texts[3].configure(text=(' %d' + degree_sign) % weather.ecart_saisonnier)
    label_weather_texts[4].configure(text=(' %d%%') % weather.pluie)


    # call itself
    root.after(1000, functools.partial(Refresher,root,bus_checker,weather,objects)) # every second...

    # set to full screen
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.attributes('-fullscreen', True)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set() # <-- move focus to this widget
    root.bind("<Escape>", lambda e: e.widget.quit())


def get_images (bus_checker):
    images = {}
    for k,_ in bus_checker.urls.iteritems():
        images[k] = ImageTk.PhotoImage(Image.open('/home/koch/nestor/img/%s.png' % k))
    
    images['morning'] = ImageTk.PhotoImage(Image.open('/home/koch/nestor/img/morning.png'))
    images['afternoon'] = ImageTk.PhotoImage(Image.open('/home/koch/nestor/img/afternoon.png'))
    images['evening'] = ImageTk.PhotoImage(Image.open('/home/koch/nestor/img/evening.png'))
    images['umbrella'] = ImageTk.PhotoImage(Image.open('/home/koch/nestor/img/umbrella.png'))
    images['difference'] = ImageTk.PhotoImage(Image.open('/home/koch/nestor/img/difference.png'))

    return images


def main():
    # transport schedule
    bus_checker = BusChecker()
    bus_checker.refresh()

    # weather
    weather = Weather()
    weather.refresh()

    root = tk.Tk()

    # get images
    images = get_images (bus_checker)

    objects = Draw(root, bus_checker, images)
    Refresher(root, bus_checker, weather, objects)
    root.mainloop()


if __name__ == "__main__":
    main()
