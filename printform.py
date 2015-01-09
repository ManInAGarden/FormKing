from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

import platform
import subprocess

# if platform.system() == "Windows":
#    import win32api

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
        self.pdf_name = None

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

        # c.showPage()
        c.save()
        self.pdf_name = name

    def get_fonts(self):
        c = canvas.Canvas("noname")
        fonts = c.getAvailableFonts()
        return fonts

    def print_pdf(self, printer_name: str=None):
        """
        print a previously created pds file to a printer
        :param printer_name: the printer to which the doc shal be printed. If not supplied standard printer will be used
        :return: Trie when document was send to the printer succesfully
        """

        if printer_name is not None:
            raise Exception("Printing to a printer other than standard is not yet implemented")

        sys_name = platform.system()
        if sys_name == "Linux":
            done = self.print_on_linux(self.pdf_name)
        elif sys_name == "Windows":
            done = self.print_on_windows(self.pdf_name)
        elif sys_name == "Darwin": # we're on a Mac
            done = self.print_on_mac(self.pdf_name)

        return done

    def print_on_linux(self, filename):
        pass

    def print_on_windows(self, filename):
        # win32api.ShellExecute(0, "print", filename, None,  ".",  0)
        lpr = subprocess.Popen(filename)
        return True

    def print_on_max(self, filename):
        # I have no idea how to print on a mac
        return False

if __name__ == "__main__":
    prt = PrintFile()
    prt.create_pdf("tst.pdf")
