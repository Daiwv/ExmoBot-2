# -*- coding: utf-8 -*-
from Tkinter import *

def reset(entry_fist_currency, entry_second_currency):
    entry_fist_currency.delete(0, END)
    entry_second_currency.delete(0, END)
    entry_fist_currency.insert(0, f_string.get_str_currency(FIRST_CURRENCY))
    entry_second_currency.insert(0, f_string.get_str_currency(SECOND_CURRENCY))

def main_():
    root = Tk()
    entry_fist_currency = Entry(root)
    entry_second_currency = Entry(root)
    root.title("EXMO-Bot")
    root.geometry('500x500')
    v_1 = IntVar()
    v_1.set(1)  # initializing the choice, i.e. Python
    v_2 = IntVar()
    v_2.set(2)  # initializing the choice, i.e. Python

    languages_1 = [("BTC", 0),("ETH", 1), ("USD", 2), ("RUB", 3)]

    languages_2 = [("USD", 2), ("RUB", 3), ("BTC", 0) ]

    def ShowChoice_1():
        print v_1.get()

    def ShowChoice_2():
        print v_2.get()

    l_first_currency = Label(root, text ='FIRST CURRENCY', bg='gray', width=15)

    l_first_currency.pack(anchor=W )


    for txt, val in languages_1:
       Radiobutton(root,
                  text=txt,
                  indicatoron=0,
                  width=10,
                  padx=2,
                  variable=v_1,
                  command=ShowChoice_1,
                  value=val).pack(anchor=W )

    l_second_currency = Label(root, text='SECOND CURRENCY', bg='gray', width=15)
    l_second_currency.pack(anchor=W )

    for txt, val in languages_2:
       Radiobutton(root,
                  text=txt,
                  indicatoron=0,
                  width=10,
                  padx=2,
                  variable=v_2,
                  command=ShowChoice_2,
                  value=val).pack(anchor=W )

    var = StringVar()
    c = Checkbutton(
        root, text="USE SECOND PAIR", variable=var,
        onvalue="RGB", offvalue="L"
    ).place(x=150, y=0)

    #reset(entry_fist_currency, entry_second_currency)

    btn_enter = Button(root, text="Enter")
    btn_enter.bind('<Button-1>', lambda event: close_window(root))
    btn_enter.place(x=200, y=400)

    btn_reset = Button(root, text="Reset")
    btn_reset.bind('<Button-1>', lambda event: reset(entry_fist_currency, entry_second_currency))
    btn_reset.place(x=300, y=400)

    #v = IntVar()

    #Radiobutton(root, text="One", variable=v, value=1).place(x=300, y=10)
    #Radiobutton(root, text="Two", variable=v, value=2).place(x=300, y=30)


    root.mainloop()


def read_gui():
    print ''
    #global FIRST_CURRENCY
    #global SECOND_CURRENCY
    #FIRST_CURRENCY  =  entry_fist_currency.get()
    #SECOND_CURRENCY = entry_second_currency.get()

def close_window (root):
    read_gui()
    root.destroy()
    start()