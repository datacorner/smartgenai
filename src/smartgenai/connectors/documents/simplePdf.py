__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import fitz # pip install PyMuPDF
from src.smartgenai.framework.documents.documentBaseObject import documentBaseObject

class simplePdf(documentBaseObject):
    def __init__(self):
        self.__fromPage = 0
        self.__toPage = 0
        self.__heightToRemove = 0
        super().__init__()

    def init(self):
        self.setCaptureBox(self.getParameterValue("fromPage", 0), 
                           self.getParameterValue("toPage", 0),
                           self.getParameterValue("heightToRemove", 0))

    def setCaptureBox(self, fromPage=0, toPage=0, heightToRemove=0):
        self.__fromPage = fromPage
        self.__toPage = toPage
        self.__heightToRemove = heightToRemove

    def load(self):
        """ Read a pdf file and add the content as text by using PyMuPDF
        Args:
            fromPage (int, optional): Starts from page Number. Defaults to 0.
            toPage (int, optional): Ends at page Number. Defaults to 0.
            heightToRemove (int, optional): Height in pixel to remove (header and footer). Defaults to 0.

        Returns:
            bool: True if no errors
        """
        try:
            self.logInfo("Read a pdf file and add the content as text by using PyMuPDF.")
            if (self.id == None):
                raise Exception("A filename must me specified")
            reader = fitz.open(self.id)
            self.logInfo("Number of pages in the document {}".format(len(reader)))
            for numPage, page in enumerate(reader): # iterate the document pages
                self.__toPage = len(reader) if (self.__toPage == 0) else self.__toPage 
                if (numPage+1 >= self.__fromPage and numPage+1 <= self.__toPage):
                    self.logInfo("Read page {}".format(str(numPage)))
                    pageBox = page.artbox
                    rect = fitz.Rect(pageBox[0], 
                                    pageBox[1] + self.__heightToRemove, 
                                    pageBox[2], 
                                    pageBox[3] - self.__heightToRemove)
                    self.content = self.content + page.get_textbox(rect) # get plain text encoded as UTF-8
        except Exception as e:
            self.logInfo("Error while reading the document: {}".format(str(e)))
            self.content = ""
            raise
