from tkinter import *

import Main
import Parsing
import Scraper
import Sqlite

root = Tk()

e = Entry(root, width=100)
e.pack()





def myClick():
    parse = Parsing.main(e.get())
    # Scraper.main(parse['v'][0])
    # Main.main()
    next_window = Toplevel()
    main_frame = Frame(next_window)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    w = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    w.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=w.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondary_frame = Frame(canvas)

    canvas.create_window((0, 0), window=secondary_frame, anchor="nw")

    records = Sqlite.query('constructive')
    for record in records:
        frame = Frame(secondary_frame)
        frame.pack()
        picture = Frame(frame)
        picture.pack(side=LEFT)
        comment = Frame(frame)
        comment.pack(side=LEFT)

        details = Frame(comment)
        details.pack(side=TOP)
        name = Frame(details)
        name.pack(side=LEFT)
        sub = Frame(details)
        sub.pack(side=RIGHT)

        bottom = Frame(comment)
        bottom.pack(side=BOTTOM)
        likes = Frame(bottom)
        likes.pack(side=RIGHT)

        name_label = Label(name, text=record[5])
        sub_label = Label(sub, text=record[2])
        likes_label = Label(likes, text=record[4])
        text_label = Label(comment, text=record[6], wraplength=250)

        name_label.pack()
        sub_label.pack()
        likes_label.pack()
        text_label.pack()


button_1 = Button(root, text="Start Algo", command=myClick)
button_1.pack()
root.mainloop()
