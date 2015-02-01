from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import platform
import subprocess

# if platform.system() == "Windows":
#    import win32api

class PrintFile():
    """
    class to support printing into forms. This is done by creating a pfd
    first which can then be printed
    """
    def __init__(self, elements, data, pagesize=(10, 150), fontname="Courier", fontsize=12):
        """
        init a new instance of Printfile
        :param fontname: Name for the font to be used in thins form
        :param fontsize: Size of font o be used throughout the form
        :param pagesize: pagesize for the form as (width, height)
        :param elements: dict of defining elements all of class GUIElement
        :type elements: dict
        :param data: dict containing the data to pe printed
        :type data: dict
        :return:
        """
        self.data = data
        self.elements = elements
        self.pdf_name = None
        self.font_name = fontname
        self.font_size = fontsize
        self.page_width, self.page_height = pagesize

    def create_pdf(self, name: str):
        """
        create a pdf with the given name
        :param name: name of the pdf to be created
        :return: nothing
        """
        c = canvas.Canvas(name, pagesize=(141.0*mm, 100.0*mm))
        # would move the origin to 1,1 mm. We don't need that here c.translate(mm, mm)
        c.setFont(self.font_name, self.font_size)
        for key, dat in self.data.items():
            el = self.elements[key]
            if el.docpos != (0, 0):
                posx, posy = el.docpos
                for single in dat:
                    c.drawString(mm*posx, mm*posy, single)
                    posx += el.letterspacing

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
        done = False

        if sys_name == "Linux":
            done = self.print_on_linux(self.pdf_name)
        elif sys_name == "Windows":
            done = self.print_on_windows(self.pdf_name)
        elif sys_name == "Darwin":  # we're on a Mac
            done = self.print_on_mac(self.pdf_name)

        return done

    def print_on_linux(self, filename):
        curd = os.path.curdir
        fullfile = curd + "/" + filename
        pr = subprocess.Popen(["lp", fullfile])

    def print_on_windows(self, filename):
        # win32api.ShellExecute(0, "print", filename, None,  ".",  0)
        # lp = subprocess.Popen(filename)
        return False

    def print_on_max(self, filename):
        # I have no idea how to print on a mac
        return False

if __name__ == "__main__":
    prt = PrintFile()
    prt.create_pdf("tst.pdf")
