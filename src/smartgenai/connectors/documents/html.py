__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.framework.documents.documentBaseObject import documentBaseObject
from langchain_community.document_loaders import WebBaseLoader
import smartgenai.utils.CONST as C

class html(documentBaseObject):
    def __init__(self):
        super().__init__()

    def load(self):
        """ read a file (text) and get the content from
        Args:
            filename (str): file name and path
        Returns:
            bool: True if ok
        """
        try:
            if (self.id == None):
                raise Exception("An URL must me specified")
            self.logInfo("Load URL {}".format(self.id))
            loader = WebBaseLoader(self.id)
            data = loader.load()
            self.content = data[0].page_content
            return True
        except Exception as e:
            self.logError("Error while loading the document: {}".format(e))
            return False