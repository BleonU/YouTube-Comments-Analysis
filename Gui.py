import webbrowser

import PIL
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
from tkinter import *


import Main
import Parsing
import Scraper
import Sqlite

root = Tk()

e = Entry(root, width=100)
e.pack()

records = []
images = {}
links = {}
variables = {}


def callback(url):
    webbrowser.open_new(url)


def myClick():
    parse = Parsing.main(e.get())
    # Scraper.main(parse['v'][0])
    # Main.main()
    records = Sqlite.query(None)
    for record in records:
        response = requests.get(record[7])
        img_data = response.content
        img = ImageTk.PhotoImage(PIL.Image.open(BytesIO(img_data)).resize((50, 50)))
        images[record[0]] = img
        links[record[0]] = 'https://www.youtube.com/channel/' + str(record[8])
    next_window = Toplevel()
    main_frame = Frame(next_window)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame, height=800, width=550)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    w = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    w.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=w.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondary_frame = Frame(canvas)
    button_menu = Frame(secondary_frame)
    button_menu.pack(side=TOP, fill=X)
    pos = Button(button_menu, text="Positive", command=lambda: getPos(next_window))
    neg = Button(button_menu, text="Negative", command=lambda: getNeg(next_window))
    con = Button(button_menu, text="Constructive", command=lambda: getCon(next_window))

    pos.pack()
    neg.pack()
    con.pack()

    canvas.create_window((0, 0), window=secondary_frame, anchor="nw")

def getPos(window):
    records = Sqlite.query('positive')
    getComments(records, window)

def getCon(window):
    records = Sqlite.query('constructive')
    getComments(records, window)

def getNeg(window):
    records = Sqlite.query('negative')
    getComments(records, window)

def getComments(records, window):
    next_window = Toplevel()
    main_frame = Frame(next_window)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame, height=800, width=550)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    w = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    w.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=w.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondary_frame = Frame(canvas)
    button_menu = Frame(secondary_frame)
    button_menu.pack(side=TOP, fill=X)
    pos = Button(button_menu, text="Positive", command=lambda: getPos(next_window))
    neg = Button(button_menu, text="Negative", command=lambda: getNeg(next_window))
    con = Button(button_menu, text="Constructive", command=lambda: getCon(next_window))

    pos.pack()
    neg.pack()
    con.pack()

    canvas.create_window((0, 0), window=secondary_frame, anchor="nw")
    i = 0

    buttons = dict()
    for record in records:
        frame = Frame(secondary_frame, width=550)
        frame.pack(anchor="w", expand=True, fill=X)
        picture = Frame(frame)
        picture.pack(side=LEFT, anchor="n")
        comment = Frame(frame, width=500)
        comment.pack(side=LEFT, anchor="w", expand=True, fill=X)

        details = Frame(comment, width=500)
        details.pack(side=TOP, anchor="w")
        name = Frame(details, width=250)
        name.pack(side=TOP, anchor="w")
        sub = Frame(details, width=250)
        sub.pack(side=BOTTOM, anchor="w")

        bottom = Frame(comment)
        bottom.pack(side=BOTTOM, anchor="e", fill=X)
        likes = Frame(bottom, width=500)
        likes.pack(side=RIGHT)

        # raw_data = urllib.request.urlopen(record[7]).read()
        # im = Image.open(io.BytesIO(raw_data))
        # imag = ImageTk.PhotoImage(im)
        # cv = Canvas(picture, bg='white')
        # cv.pack(side=LEFT, fill=BOTH, expand=1)
        # cv.create_image(10, 10, image=imag, anchor='nw')

        # response = requests.get(record[7])
        # img_data = response.content
        # img = ImageTk.PhotoImage(PIL.Image.open(BytesIO(img_data)))
        panel = Label(picture, image=images.get(record[0]))
        panel.pack(side="bottom", fill="both", expand="yes")

        buttons[record[0]] = Button(name, text=record[5],
                                    command=lambda a=record[0]: callback(links.get(a)), borderwidth=0)

        sub_label = Label(sub, text='Subscriber Count: ' + str(record[2]))
        likes_label = Label(likes, text='Likes: ' + str(record[4]))
        text_label = Label(comment, text=record[6], wraplength=500, anchor="w")

        buttons[record[0]].pack()
        sub_label.pack()
        likes_label.pack()
        text_label.pack()

        window.destroy()
        # if records.index(record) == len(records)-1: lets_crash.pack()


button_1 = Button(root, text="Start Algo", command=myClick)
button_1.pack()
root.mainloop()
