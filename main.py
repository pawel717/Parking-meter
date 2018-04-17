import random
from tkinter import *
from tkinter import messagebox
from Model import *
from View import *
from time import localtime, strftime
import time, datetime

class Controller(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.title(self, "Parkomat")
        container = Frame(self)
        container.pack()
        self.minsize(width=300, height=200)
        self.resizable(width=False, height=False)
        self.frames = {}
        for F in (firstview.FirstView, secondview.SecondView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky=N+E+W+S)
            frame.bind("<<ShowView>>", frame.reset)
        self.bindButtons()
        self.totalPaid = cash.Total()
        self.totalIn = cash.Total()
        self.isValid = True
        self.show_frame("FirstView")

    def bindButtons(self):
        self.frames['FirstView'].payButton.config(command=lambda: self.payAction(self.frames['FirstView']))
        self.frames['FirstView'].outDateEntry.bind("<FocusOut>", lambda event: self.outDateAction(self.frames['FirstView']))
        self.frames['SecondView'].button1gr.config(command = lambda: self.cashAction(self.frames['SecondView'], "gr", 1))
        self.frames['SecondView'].button2gr.config(command = lambda: self.cashAction(self.frames['SecondView'], "gr", 2))
        self.frames['SecondView'].button5gr.config(command = lambda: self.cashAction(self.frames['SecondView'], "gr", 5))
        self.frames['SecondView'].button10gr.config(command = lambda: self.cashAction(self.frames['SecondView'], "gr", 10))
        self.frames['SecondView'].button20gr.config(command = lambda: self.cashAction(self.frames['SecondView'], "gr", 20))
        self.frames['SecondView'].button50gr.config(command = lambda: self.cashAction(self.frames['SecondView'], "gr", 50))
        self.frames['SecondView'].button1zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "zl", 1))
        self.frames['SecondView'].button2zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "zl", 2))
        self.frames['SecondView'].button5zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "zl", 5))
        self.frames['SecondView'].button10zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "bill", 10))
        self.frames['SecondView'].button20zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "bill", 20))
        self.frames['SecondView'].button50zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "bill", 50))
        self.frames['SecondView'].button100zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "bill", 100))
        self.frames['SecondView'].button200zl.config(command = lambda: self.cashAction(self.frames['SecondView'], "bill", 200))
        self.frames['SecondView'].buttonCreditCard.config(command=lambda: self.creditCardAction(self.frames['SecondView']))

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.event_generate("<<ShowView>>")
        frame.tkraise()

    def payAction(self, view):
        if not self.isValid:
            messagebox.showerror("Ups...", "Niepoprawna data")
        elif view.registrationVar.get()=="":
            messagebox.showerror("Ups...", "Uzupełnij pole 'Numer rejestracyjny'")
        else:
            self.frames['SecondView'].amountToPayVar.set(view.amountToPayVar.get())
            self.show_frame("SecondView")

    def outDateAction(self, view, *args):
        inDate = datetime.datetime.strptime(view.inDateVar.get(), "%d-%m-%Y %H:%M")
        try:
            outDate = datetime.datetime.strptime(view.outDateVar.get(), "%d-%m-%Y %H:%M")  # wyjatek
            if outDate <= inDate:
                raise ValueError
        except ValueError:
            self.isValid = False
        else:
            self.isValid = True
            parkTime = parktime.ParkTime(inDate, outDate)
            view.amountToPayVar.set(parkTime.getTotalPrice())

    def creditCardAction(self, view):
        chance = random.randrange(100)
        if chance < 1:
            messagebox.showerror("Ups...","Transakcja odrzucona")
        else:
            messagebox.showinfo("Paragon","Drukowanie paragonu...\nZapłacono: {0:}\nReszta: {1:}".format(view.amountPaidVar.get(), self.totalPaid.get_total()))
            self.finishPayment()

    def cashAction(self, view, buttonName, value):
        if buttonName == "gr":
            self.totalPaid.add(cash.CoinGr(value))
        elif buttonName == "zl":
            self.totalPaid.add(cash.CoinZl(value))
        else:
            self.totalPaid.add(cash.Bill(value))
        view.amountPaidVar.set(self.totalPaid.get_total())
        view.ballanceVar.set(round(view.amountToPayVar.get() - view.amountPaidVar.get(), 2))
        if view.ballanceVar.get() <= 0:
            view.changeVar.set(abs(view.ballanceVar.get()))
            view.ballanceVar.set(0)
            if self.totalIn.giveChange(self.totalPaid, view.changeVar.get()):
                messagebox.showinfo("Paragon","Drukowanie paragonu...\nZapłacono: {0:}\nReszta: {1:}".format(view.amountPaidVar.get(), view.changeVar.get()))
            else:
                messagebox.showerror("Ups...", "Tylko odliczona kwota \nZwrot: {0:}".format(view.amountPaidVar.get()))
            self.finishPayment()

    def finishPayment(self):
        self.totalPaid.removeAll()
        self.show_frame("FirstView")

app = Controller()
app.mainloop()