# -*- coding: utf-8 *-*
# made for python3!

from tkinter import *
from tkinter.ttk import *


class TkWindow():

    registers = {}

    def __init__(self, parent, title, width=400, height=300):
        self.parent = parent #Tk or toplevel
        self.w = width
        self.h = height
        self.make_gui(title)
        self.loaded()

    def loaded(self):
        pass # overload me

    """register another window to receive a signal"""
    @classmethod
    def register_sig(cls, target, signame):
        if not target in cls.registers:
            cls.registers[target] = []

        cls.registers[target].append(signame)

    """send a signal to all registered windows"""
    def send_sig(self, signame, data=None):
        cls = self.__class__
        for targ, sigs in cls.registers.items():
            if sigs != None:
                if signame in sigs:
                    targ.receive(self, signame, data)

    """receive a signame"""
    def receive_sig(self, sender, signame, data):
        print("receive not overloaded but signal registered for <"
              + signame + "> from <"
              + str(sender) + "> with <" + str(data) +">")
        # overload me in your receiving window for your application

    """overloading register to make code look better"""
    def register(self, regwhat):
        return self.frame.register(regwhat)

    def make_gui(self, title):
        self.parent.title(title)
        Style().configure("TFrame", pad=5)
        Style().configure("TButton", relief="flat", padx=5, pady=5)
        self.frame = Frame(self.parent,
            width=self.w,
            height=self.h)


    def makelabel(self, parent, lpos=(0, 0), lspan=(1, 1), caption='', lstick=E, **options):
        lcol, lrow = lpos
        lcolspan, lrowspan = lspan
        lab = Label(parent, text=caption, **options)
        lab.grid(row=lrow, column=lcol, sticky=lstick, columnspan=lcolspan, rowspan=lrowspan)
        return lab

    """create a multiline text entry field with a label"""
    def maketext(self, parent, lpos=(0,0), epos=(0, 1), caption='', width=None, lstick=NE, estick=W, **options):
        lcol, lrow = lpos
        ecol, erow = epos

        if caption != '':
            Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=lstick)

        entry = Text(parent, **options)
        if width:
            entry.config(width=width)

        entry.grid(row=erow, column=ecol, sticky=estick)
        return entry

    def makeentry(self, parent, lpos=(0, 0), epos=(0, 1), lspan=(1, 1), espan=(1, 1), caption='', lstick=E, estick=W, width=None, **options):
        lcol, lrow = lpos
        ecol, erow = epos
        lcolspan, lrowspan = lspan
        ecolspan, erowspan = espan
        if caption != '':
            Label(parent, text=caption).grid(row=lrow, column=lcol, rowspan=lrowspan, columnspan=lcolspan, sticky=lstick)

        entry = Entry(parent, **options)
        if width:
            entry.config(width=width)

        entry.grid(row=erow, column=ecol, columnspan=ecolspan, rowspan=erowspan, sticky=estick)
        return entry

    def setentryvalue(self, entry, value):
        entry.delete(0, END)
        entry.insert(0, value)

    def settextvalue(self, entry, value):
        entry.delete(0.0, END);
        entry.insert(0.0, value);

    def setbuttontext(self, button, txt):
        button['text'] = txt

    def makecombo(self, parent, cpos=(1,0) , lpos=(0, 0), caption='',
                  width=None, **options):
        ccol, crow = cpos
        lcol, lrow = lpos
        if caption != '':
            Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=E)

        cbox = Combobox(parent, **options)

        if width:
            cbox.config(width=width)

        cbox.grid(row=crow, column=ccol)

        return cbox


    def makecheck(self, parent, epos=(0, 0), caption='', **options):
        ecol, erow = epos
        cb = Checkbutton(parent, text=caption, **options)
        cb.grid(row=erow, column=ecol, sticky=W)
        return cb

    def makebutton(self, parent, bpos=(0, 0), caption='Press me', sticky=W, **options):
        bcol, brow = bpos
        bu = Button(parent, text=caption, **options)
        bu.grid(row=brow, column=bcol, sticky=sticky)
        return bu

    """create a list at the givne position"""
    def makelist(self, parent, llpos=(0, 1), lpos=(0,0),
                 caption='List', elements=[], mode='v',
                 lspan=(1, 1),
                 **options):

        lcol, lrow = lpos
        llco, llrow = llpos
        lcolspan, lrowspan = lspan
        frame = Frame(parent)
        frame.grid(row=lrow, column=lcol, rowspan=lrowspan, columnspan=lcolspan)

        hscroll = vscroll = None

        if caption!='':
            Label(parent, text=caption).grid(row=llrow, column=llcol, sticky=W)

        lb = Listbox(frame, **options)


        if 'v' in mode:
            vscroll = Scrollbar(frame, orient=VERTICAL)
            lb.config(yscrollcommand = vscroll.set)
            vscroll.config(command=lb.yview)
            vscroll.pack(side=RIGHT, fill=Y)

        if 'h' in mode:
            hscroll = Scrollbar(frame, orient=HROZONTAL)
            lb.configure(xscrollcommand = hscroll.set)
            hscroll.config(command = lb.xview)
            hscroll.pack(side=BOTTOM, fill=X)

        lb.pack(side=LEFT, fill=BOTH, expand=1)

        if len(elements)>0:
            self.setlistelements(elements)

        return lb


    def setlistelements(self, lb, elements):
        lb.delete(0, END)
        for element in elements:
            lb.insert(END, element)



