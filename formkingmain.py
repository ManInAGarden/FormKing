from tkwindow import *
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as messagebox
import configparser as confp

CONFIG_FILE_NAME = "FormKing.cfg"

class FormKingWindow(TkWindow):

    def __init__(self, parent, title, width=400, height=300):
        self.form_title = ""
        self.elements = {}
        self.widgets = {}
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

        :type tst: str
        """
        if ',' not in tst:
            return False

        comidx = tst.index(',')
        if comidx < 0:
            return False

        return True

    def validate(self, widname, value):
        """
        validates a value to what is defined in elements for
        widname
        :type widname: str
        :type value: str
        """
        print("validating <" + str(value) + ">")
        # in dubio pro reo
        self.widgets[widname].configure(foreground="black")

        el = self.elements[widname]
        valm = el.valuetype
        if valm is None:
            return True
        if valm == "none":
            return True
        if valm == "text":
            return True
        if valm == "currency":
            return self.iscurrency(value)

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
        # Style().configure("TEntry", font="systemfixed 18 normal")
        for key, el in self.elements.items():
            lstick, estick = el.stick
            lastcol, lastrow = self.check_cells(el, (lastcol, lastrow))
            if el.wid_type == "ENTRY":
                self.widgets[el.name] = self.makeentry(self.frame,
                                                       lpos = el.label_position,
                                                       epos = el.widget_position,
                                                       lspan = el.label_span,
                                                       espan = el.widget_span,
                                                       lstick = lstick,
                                                       estick = estick,
                                                       caption=el.caption,
                                                       width=el.width,
                                                       font="courier 12")
                # %W - entry widget name
                # %P - entry string
                self.setentryvalue(self.widgets[el.name], el.default)
                self.widgets[el.name].config(validate="focusout",
                                             validatecommand=(self.register(self.validate), el.name, "%P"),
                                             invalidcommand=(self.register(self.invalid), el.name))
            elif el.wid_type == "LABEL":
                self.widgets[el.name] = self.makelabel(self.frame,
                                                       lpos=el.label_position,
                                                       lspan=el.label_span,
                                                       caption=el.caption)

        print_bu = self.makebutton(self.frame, caption="Print", bpos=(0, lastrow + 1),
                                   command=self.print_cb)
        exit_bu = self.makebutton(self.frame, caption="Exit", bpos=(lastcol, lastrow + 1),
                                  command=self.exit_cb)

        self.parent.config(padx=5, pady=5)
        lastrow += 1

        for row in range(0, lastrow + 1):
            self.frame.rowconfigure(row, pad=5)
        for col in range(0, lastcol + 1):
            self.frame.columnconfigure(col, pad=5)

        titlab.grid(columnspan=lastcol+1)
        self.frame.pack()


    def print_cb(self):
        raise Exception("not yet implemented")

    def exit_cb(self):
        if messagebox.askyesno("Frage", "Wirklich beenden?", parent=self.frame):
            self.parent.destroy()


class GUIElement:
    def __init__(self):
        self.name = ""
        self.wid_type = ""
        self.label_position = (0, 1)
        self.label_span = (1, 1)
        self.widget_position = (0, 1)
        self.widget_span = (1, 1)
        self.width = 5
        self.caption = ""
        self.stick = ("E", "W")
        self.default = ""
        self.valuetype = None

    def __str__(self):
        lstick, estick = self.stick
        return "{0} is {1}\nlabel: {2} span {3} stick {6}\nentry:{4} span {5} stick {7}".format(self.name,
                                     self.wid_type,
                                     self.label_position, self.label_span,
                                     self.widget_position, self.widget_span,
                                     lstick,
                                     estick)

    def prepare_string(self, ins):
        answ = ins.replace("#COMMA#", ",")
        return answ.strip()

    def read_from_string(self, line):
        """
        :type line: str
        :param line: string represantation of a tk gui element
        :return: nothing
        """
        strrep = line.replace("\,", "#COMMA#")
        parts = strrep.split(",")
        #print("processing " + str(parts))
        p = 0
        self.name = self.prepare_string(parts[p])
        p += 1
        self.wid_type = self.prepare_string(parts[p])
        p += 1
        self.caption = self.prepare_string(parts[p])
        p += 1
        self.label_position = (int(parts[p]), int(parts[p + 1]) + 1)
        p += 2
        self.label_span = (int(parts[p]), int(parts[p + 1]))
        p += 2
        labelstick = parts[p].strip()
        p += 1
        self.widget_position = (int(parts[p]), int(parts[p + 1]) + 1)
        p += 2
        self.widget_span = (int(parts[p]), int(parts[p + 1]))
        p += 2
        widgetstick = parts[p].strip()
        p += 1
        self.width = int(parts[p].strip())
        p += 1
        self.height = int(parts[p].strip())
        p += 1
        self.default = self.prepare_string(parts[p])
        p += 1
        self.valuetype = parts[p].strip()

        self.stick = labelstick, widgetstick
        print(self)

if __name__ == "__main__":
    root = Tk()
    mainw = FormKingWindow(root, "Form-King")
    root.mainloop()
