__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.framework.documents.documentBaseObject import documentBaseObject
import smartgenai.utils.CONST as C

class txt(documentBaseObject):
    def __init__(self):
        self.__filename = None
        super().__init__()

    @property
    def filename(self):
        return self.__filename
    @filename.setter
    def filename(self, q):
        self.__filename = q
        
    def load(self):
        """ read a file (text) and get the content from
        Args:
            filename (str): file name and path
        Returns:
            bool: True if ok
        """
        try:
            if (self.filename == None):
                raise Exception("A filename must me specified")
            self.logInfo("Load document with filename: {}".format(self.filename))
            with open(self.filename, "r", encoding=C.ENCODING) as f:
                self.content = f.read()
            self.logInfo("Document loaded successfully.")
            return True
        except Exception as e:
            self.logError("Error while loading the document: {}".format(e))
            return False