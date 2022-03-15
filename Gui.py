import webbrowser
# from profanity_filter import ProfanityFilter
import numpy as np
from better_profanity import profanity

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
e.pack(side=LEFT)

records = []
images = {}
links = {}


def callback(url):
    webbrowser.open_new(url)


def close(window, button, button2):
    button2['state'] = NORMAL

    button.destroy()
    window.destroy()


def start():
    parse = Parsing.main(e.get())
    # Scraper.main(parse['v'][0])
    # Main.main()
    comments = Button(root, text="Show Comments", command=lambda: show_comments(comments, start_algo))
    comments.pack(side=BOTTOM)




def show_comments(button, button2):
    button['state'] = DISABLED
    button2['state'] = DISABLED

    records = Sqlite.query(None, 'Comments')
    for record in records:
        response = requests.get(record[7])
        img_data = response.content
        img = ImageTk.PhotoImage(PIL.Image.open(BytesIO(img_data)).resize((50, 50)))
        images[record[0]] = img
        links[record[0]] = 'https://www.youtube.com/channel/' + str(record[8])
    window = Toplevel()
    main_frame = Frame(window)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame, height=800, width=550)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    w = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    w.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=w.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=main_frame.bbox("all")))

    secondary_frame = Frame(canvas)
    button_menu = Frame(secondary_frame)
    button_menu.pack(side=TOP, fill=X)

    option = StringVar(value="uncensored")
    likes = StringVar(value="off")
    subs = StringVar(value="off")

    Checkbutton(button_menu, text="Likes", variable=likes, onvalue="on", offvalue="off").pack(side=RIGHT)
    Checkbutton(button_menu, text="Subs", variable=subs, onvalue="on", offvalue="off").pack(side=RIGHT)

    Radiobutton(button_menu, text="Censored", variable=option, value="censor").pack(side=RIGHT)
    Radiobutton(button_menu, text="Uncensored", variable=option, value="uncensored").pack(side=RIGHT)
    Radiobutton(button_menu, text="Clean", variable=option, value="clean").pack(side=RIGHT)

    parameters = [main_frame, option, likes, subs, window, button, button2]

    Button(button_menu, text="Positive", command=lambda: getComments('positive', parameters)).pack(side=LEFT)
    Button(button_menu, text="Negative", command=lambda: getComments('negative', parameters)).pack(side=LEFT)
    Button(button_menu, text="Constructive", command=lambda: getComments('constructive', parameters)).pack(side=LEFT)

    canvas.create_window((0, 0), window=secondary_frame, anchor="nw")
    window.protocol("WM_DELETE_WINDOW", lambda: close(parameters[4], parameters[5], parameters[6]))



def get_replies(cid, censor):
    next_window = Toplevel()
    main_frame = Frame(next_window)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame, height=800, width=600)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    w = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    w.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=w.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondary_frame = Frame(canvas)
    canvas.create_window((0, 0), window=secondary_frame, anchor="nw")

    replies = Sqlite.query("""original_comment_id = '""" + cid, 'Replies')
    records = []
    for reply in replies:
        for l in Sqlite.query("""cid = '""" + reply[1], 'Comments'):
            records.append(l)
    build_comments(records, secondary_frame, censor)


def build_comments(records, secondary_frame, censor):
    buttons = dict()
    replies = dict()
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
        reply = Frame(bottom, width=250)
        reply.pack(side=LEFT)
        likes = Frame(bottom, width=250)
        likes.pack(side=RIGHT)

        panel = Label(picture, image=images.get(record[0]))
        panel.pack(side="bottom", fill="both", expand="yes")
        buttons[record[0]] = Button(name, text=record[5],
                                    command=lambda a=record[0]: callback(links.get(a)), borderwidth=0)

        if record[2] is -1:
            subscribers = 'HIDDEN'
        else:
            subscribers = record[2]

        sub_label = Label(sub, text='Subscriber Count: ' + str(subscribers))
        likes_label = Label(likes, text='Likes: ' + str(record[4]))
        replies[record[0]] = Button(name, text='Replies: ' + str(record[3]),
                                    command=lambda a=record[0]: get_replies(a, censor), borderwidth=0)
        # pf = ProfanityFilter(languages=['en'])
        if censor.get() == "censor":
            # pf.censor_char = '*'
            text_label = Label(comment, text=profanity.censor(record[6]), wraplength=500, anchor="w")
        elif censor.get() == "clean":
            # pf.censor_char = ''
            text_label = Label(comment, text=profanity.censor(record[6], ''), wraplength=500, anchor="w")
        else:
            text_label = Label(comment, text=record[6], wraplength=500, anchor="w")

        buttons[record[0]].pack()
        replies[record[0]].pack()
        sub_label.pack()
        likes_label.pack()
        text_label.pack()


def getComments(filter, parameters):
    records = Sqlite.query("""evaluation = '""" + filter, 'Comments')
    old_frame = parameters[0]
    censor = parameters[1]
    old_window = parameters[4]
    old_frame.destroy()

    if parameters[2].get() == "on":
        records.sort(key=lambda tup: tup[4], reverse=True)
    if parameters[3].get() == "on":
        records.sort(key=lambda tup: tup[2], reverse=True)

    main_frame = Frame(old_window)
    main_frame.pack(fill=BOTH, expand=1)

    old_window.protocol("WM_DELETE_WINDOW", lambda: close(parameters[4], parameters[5], parameters[6]))

    canvas = Canvas(main_frame, height=800, width=600)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    w = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    w.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=w.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondary_frame = Frame(canvas)
    button_menu = Frame(secondary_frame)
    button_menu.pack(side=TOP, fill=X)

    likes = StringVar(value="off")
    subs = StringVar(value="off")

    Checkbutton(button_menu, text="Likes", variable=likes, onvalue="on", offvalue="off").pack(side=RIGHT)
    Checkbutton(button_menu, text="Subs", variable=subs, onvalue="on", offvalue="off").pack(side=RIGHT)

    option = StringVar(value=censor)

    Radiobutton(button_menu, text="Censored", variable=option, value="censor").pack(side=RIGHT)
    Radiobutton(button_menu, text="Uncensored", variable=option, value="uncensored").pack(side=RIGHT)
    Radiobutton(button_menu, text="Clean", variable=option, value="clean").pack(side=RIGHT)

    parameters = [main_frame, option, likes, subs, old_window, parameters[5], parameters[6]]

    Button(button_menu, text="Positive", command=lambda: getComments('positive', parameters)).pack(side=LEFT)
    Button(button_menu, text="Negative", command=lambda: getComments('negative', parameters)).pack(side=LEFT)
    Button(button_menu, text="Constructive", command=lambda: getComments('constructive', parameters)).pack(side=LEFT)

    canvas.create_window((0, 0), window=secondary_frame, anchor="nw")
    build_comments(records, secondary_frame, censor)


start_algo = Button(root, text="Start Algo", command=lambda: start())
start_algo.pack(side=RIGHT)
root.mainloop()
