__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import json
from numpyencoder import NumpyEncoder
import smartgenai.utils.CONST as C
from smartgenai.interfaces.IChunks import IChunks

""" Manages the Chunks file structure (JSON)
    Content = {"chunks": [..., ...] }
"""

class chunks(IChunks):
    def __init__(self):
        self.__chunks = [] # simple Array which contains all the chunks
    
    @property
    def items(self): 
        return self.__chunks 
    @items.setter
    def items(self, q):
        self.__chunks = q

    def __getitem__(self, item):
        """ Makes the Data column accessible via [] array
            example: df['colName']
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__chunks.__getitem__(item)
    
    @property
    def jsonContent(self): 
        return json.dumps(self.__createEnveloppe(), cls=NumpyEncoder)
    @jsonContent.setter
    def jsonContent(self, content):
        try:
            jsonEnv = json.loads(content)
            self.items = jsonEnv[C.JST_CHUNKS]
        except Exception as e:
            self.items = []
            raise

    @property
    def size(self): 
        return len(self.items)
    
    def __createEnveloppe(self):
        jsonEnv = {}
        jsonEnv[C.JST_CHUNKS] = self.items
        return jsonEnv
    
    def add(self, chunk):
        self.__chunks.append(chunk)
    
    def setLangchainDocument(self, lcDoc):
        """ Wrap and store the document langchain
        Args:
            docs (document): langchain document
        Returns:
            int: Number of chunks
            str: json chunks -> {'chunks': ['Transcript of ...', ...] }
        """
        self.items = [ x.page_content for x in lcDoc ]

    def save(self, filename):
        """ Save the chunks in a file.
        Args:
            filename (_type_): JSON chunks file
        Returns:
            bool: True if ok
        """
        try:
            with open(filename, "w", encoding=C.ENCODING) as f:
                f.write(self.jsonContent)
            return True
        except Exception as e:
            return False

    def load(self, filename = "", content = ""):
        """ Load and build a chunk file (can be loaded from a json file or a json content). 
            Format required : Content = {"chunks": [..., ...] }
        Args:
            filename (str, optional): JSON chunks file. Defaults to "".
            content (str, optional): JSON chunks content. Defaults to "".
        Returns:
            bool: True if ok
        """
        try:
            jsonEnv = ""
            if (len(filename) >0):
                with open(filename, "r", encoding=C.ENCODING) as f:
                    jsonEnv = json.load(f)
                self.items = jsonEnv[C.JST_CHUNKS]
            elif (len(content) >0):
                jsonEnv = content
                self.items.append(jsonEnv)
            else:
                return False
            return True
        except Exception as e:
            return False