from tkwindow import *
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as messagebox
import configparser as confp
import datetime
import platform

from guielement import *
from printform import *

CONFIG_FILE_NAME = "FormKing.cfg"

class FormKingWindow(TkWindow):

    def __init__(self, parent, title, width=400, height=300):
        self.form_title = ""
        self.entry_font = "courier 10"
        self.elements = {}
        self.widgets = {}
        self.helplabs = {}
        super().__init__(parent, title, width=width, height=height)

    def loaded(self):
        pass

    def load_conf(self, name):
        cp = confp.ConfigParser()
        cp.read(CONFIG_FILE_NAME)
        for key in cp[name]:
            if key.startswith("element"):
                elm = GUIElement()
                elm.read_from_string(cp[name][key])
                self.elements[elm.name] = elm
            elif key == "title":
                self.form_title = cp[name][key]
            elif key == "entryfont":
                self.entry_font = cp[name][key]


    def check_cells(self, element, currmax):
        """
        check the positions and spans to return the maximum cell-count
        :type element: GUIElement
        """
        mcol, mrow = currmax
        ecol, erow = element.widget_position
        lcol, lrow = element.label_position
        lcolspan, lrowspan = element.label_span
        ecolspan, erowspan = element.widget_span

        mcol = max(lcol + lcolspan, mcol)
        mcol = max(ecol + ecolspan, mcol)
        mrow = max(lrow + lrowspan, mrow)
        mrow = max(erow + erowspan, mrow)

        return mcol, mrow

    def iscurrency(self, tst):
        """
        check string for currency contents, tst must contain a comma
        have two digits behind and at least one before the comma and
        must not contain anything else but digits and a comma
        :param tst: the string to be tested
        :type tst: str
        """
        if ',' not in tst:
            return "Komme fehlt"

        comidx = tst.index(',')
        if comidx <= 0:
            return "Betrag vor dem Komma fehlt"

        if (len(tst) - comidx) != 3:  # the mysteries of integer caclulations
            return "Es müssen exakt zwei Nachkommastellen sein"

        if not tst.replace(',', '', 1).isdigit():
            print("not only digits an comma")
            return "Falsche Zeichen für einen Geldbetrag"

        return None

    def is_valid_ibanchecksum(self, iban):
        """
        check for valid iban checkum
        :param iban: the iban to check
        :return: True when checksumm is correct
        """
        calcban = iban[4:] + iban[:4]
        nums = ""
        for c in calcban:
            if c.isdigit():
                nums += c
            else:
                nums += str(ord(c)-55)

        num = int(nums)
        # print(num)
        q, r = divmod(num, 97)

        return r == 1


    def isiban(self, tst):
        """
        test for iban with correct checksum
        :param tst: value to be testet
        :type tst: str
        :return: boolean value
        """
        compact = tst.replace(" ", "")
        if len(compact) > 34:
            return "Zu viele Zeichen für eine IBAN"

        if not compact[0:1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return "Der Ländercode muss mit zwei Großbuchenstaben angegeben werden"

        if (len(compact) > 0) and not self.is_valid_ibanchecksum(compact):
            return "Prüfsummencheck: Dies ist keine gültige IBAN"

        return None

    def checklength(self, element, value):
        if len(value) > element.width:
            return "Zu viele Zeichen für diesen Wert"

        return None

    def validate(self, widname, value):
        """
        validates a value to what is defined in elements for
        widname
        :type widname: str
        :type value: str
        """
        # print("validating <" + str(value) + ">")
        # in dubio pro reo
        entry = self.widgets[widname]
        entry.configure(foreground="black")

        el = self.elements[widname]
        valm = el.valuetype
        errs = self.checklength(el, value)
        # print("<" + str(errs) + ">")
        if errs is None:
            if valm is None:
                errs = None
            if valm == "none":
                errs = None
            if valm == "text":
                errs = None
            if valm == "currency":
                errs = self.iscurrency(value)
            if valm == "iban":
                errs = self.isiban(value)

        if errs is not None:
            self.helplabs[widname].configure(text=errs, wraplength=entry.winfo_width())
        else:
            self.helplabs[widname].configure(text="")

        return errs is None

    def invalid(self, widname):
        print("invalid")
        wid = self.widgets[widname]
        wid.configure(foreground="red")

    def make_gui(self, title):
        super().make_gui(title)
        self.load_conf("DEFAULT")
        titlab = self.makelabel(self.frame, caption=self.form_title, lpos=(0, 0), lstick=W)
        titlab["font"] = "Helvetica 16 bold italic"
        lastrow = 0
        lastcol = 0
        # Style().configure("TEntry", hightlightbackground="red")
        for el in sorted(self.elements.values(), key=lambda var: var.order):
            key = el.name
            lstick, estick = el.stick
            lastcol, lastrow = self.check_cells(el, (lastcol, lastrow))
            if el.wid_type == "ENTRY":
                wid, lab = self.makehelpedentry(self.frame,
                                                lpos = el.label_position,
                                                epos = el.widget_position,
                                                lspan = el.label_span,
                                                espan = el.widget_span,
                                                lstick = lstick,
                                                estick = estick,
                                                caption=el.caption,
                                                width=el.width,
                                                font=self.entry_font)

                self.widgets[el.name] = wid
                self.helplabs[el.name] = lab
                # %W - entry widget name
                # %P - entry string
                self.setentryvalue(wid, el.default)
                wid.config(validate="focusout",
                           validatecommand=(self.register(self.validate), el.name, "%P"),
                           invalidcommand=(self.register(self.invalid), el.name))
                lab.config(foreground="red")
            elif el.wid_type == "LABEL":
                self.widgets[el.name] = self.makelabel(self.frame,
                                                       lpos=el.label_position,
                                                       lspan=el.label_span,
                                                       caption=el.caption)

        self.print_bu = self.makebutton(self.frame, caption="Print", bpos=(0, lastrow + 1),
                                   command=self.print_cb)
        self.exit_bu = self.makebutton(self.frame, caption="Exit", bpos=(lastcol, lastrow + 1),
                                  command=self.exit_cb)

        self.parent.config(padx=5, pady=5)
        lastrow += 1

        for row in range(0, lastrow + 1):
            self.frame.rowconfigure(row, pad=5)
        for col in range(0, lastcol + 1):
            self.frame.columnconfigure(col, pad=5)

        titlab.grid(columnspan=lastcol+1)
        self.frame.pack()

    def get_data_dict(self):
        answ = {}
        for key, el in self.elements.items():
            wid = self.widgets[key]
            if wid.__class__ is Entry:
                data = wid.get()
                if data is not None and len(data) > 0:
                    answ[key] = data

        return answ

    def print_cb(self):
        errors = 0
        for lab in self.helplabs.values():
            labtxt = lab["text"]
            if len(labtxt) > 0:
                errors += 1

        if errors==0 or ((errors > 0) and messagebox.askyesno("Frage", "Es wurden Fehler in der Eingabe erkannt. Trotzdem drucken?")):
            pdfname = "formking{0:%Y%m%d%H%M%S}.pdf".format(datetime.datetime.now())
            datadict = self.get_data_dict()
            prt = PrintFile(self.elements, datadict)
            prt.create_pdf(pdfname)
            prt.print_pdf()

    def exit_cb(self):
        if messagebox.askyesno("Frage", "Wirklich beenden?", parent=self.frame):
            self.parent.destroy()




if __name__ == "__main__":
    root = Tk()
    mainw = FormKingWindow(root, "Form-King")
    root.mainloop()
