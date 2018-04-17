from tkinter import *
from time import localtime, strftime
import datetime

class FirstView(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.bind_all("<1>", lambda event: event.widget.focus_set())
        self.controller = controller
        self.inDateVar = StringVar()
        self.outDateVar = StringVar()
        self.registrationVar = StringVar()
        self.amountToPayVar = DoubleVar()
        self.clockUpdate()
        self.createView()
        self.reset("<<ShowView>>")

    def createView(self):
        Label(self, text="Aktualna Data:", justify=LEFT, padx=5, pady=5).grid(row=0, column=0,)
        Label(self, textvariable=self.inDateVar, justify=LEFT, padx=5, pady=5).grid(row=0, column=1)
        Label(self, text="Data wyjazdu:", justify=LEFT, padx=5, pady=5).grid(row=1, column=0)
        self.outDateEntry = Entry(self, textvariable=self.outDateVar, justify=LEFT)
        self.outDateEntry.grid(row=1, column=1)
        Label(self, text="Numer rejestracyjny:", justify=LEFT, padx=5, pady=5).grid(row=2, column=0)
        self.registrationEntry=Entry(self, textvariable=self.registrationVar, justify=LEFT)
        self.registrationEntry.grid(row=2, column=1)
        Label(self, text="Do zaplaty:", justify=LEFT, padx=5, pady=5).grid(row=3, column=0)
        Label(self, textvariable=self.amountToPayVar).grid(row=3, column=1)
        self.payButton=Button(self, text="Zapłać", justify=CENTER, padx=100, pady=5)
        self.payButton.grid(columnspan=2, pady=20)

    def reset(self, event):
        self.amountToPayVar.set(2)
        self.outDateVar.set(datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=1), "%d-%m-%Y %H:%M"))
        self.registrationVar.set("")

    def clockUpdate(self):
        self.inDateVar.set(strftime("%d-%m-%Y %H:%M", localtime()))
        self.after(1000, self.clockUpdate)