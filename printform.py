from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from guielement import *


class PrintFile():
    """
    class to support printing into forms. This is done by creating a pfd
    first which can then be printed
    """

    def __init__(self, elements, data):
        """
        init a new instance of Printfile
        :param elements: dict of defining elements all of class GUIElement
        :type elements: dict
        :param data: dict containing the data to pe printed
        :type data: dict
        :return:
        """
        self.data = data
        self.elements = elements

    def create_pdf(self, name: str):
        """
        create a pdf with the given name
        :param name: name of the pdf to be created
        :return: nothing
        """
        c = canvas.Canvas(name, pagesize=(141.0*mm, 100.0*mm))
        # would move the origin to 1,1 mm. We don't need that here c.translate(mm, mm)
        c.setFont("Courier", 12)
        for key, dat in self.data.items():
            el = self.elements[key]
            if el.docpos != (0, 0):
                posx, posy = el.docpos
                c.drawString(mm*posx, mm*posy, dat)

        #c.showPage()
        c.save()

    def get_fonts(self):
        c = canvas.Canvas("noname")
        fonts = c.getAvailableFonts()
        return fonts

    def print_pdf(self, printername: str):
        """
        print a previously created pds file to a printer
        :param printername: the printer to which the doc shal be printed
        :return: nothing
        """
        pass

if __name__ == "__main__":
    prt = PrintFile()
    prt.create_pdf("tst.pdf")
