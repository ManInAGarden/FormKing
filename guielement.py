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
        self.docpos = (0, 0)

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
        p += 1
        self.docpos =  int(parts[p].strip()), int(parts[p + 1].strip())
        p += 2

        self.stick = labelstick, widgetstick
        print(self)
