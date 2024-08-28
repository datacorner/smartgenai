__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import json
from numpyencoder import NumpyEncoder
from smartgenai.interfaces.IEmbeddings import IEmbeddings
import smartgenai.utils.CONST as C
from smartgenai.framework.embeddings.embedding import embedding
from smartgenai.framework.objectBase import objectBase

"""
        Embeddings and data are stored in Python list/JSON and used with the following format :
        {"0": {
                'text': 'The prompt or text', 
                'embedding': array([-6.65125623e-02,  
                                    ..., 
                                    -1.22626998e-01]) 
              },
        "1": {
                'text': '...',  
                'embedding': array([...]) 
              },
        ...,
        "x" : { ... }
        }
"""

class embeddingsBaseObject(IEmbeddings, objectBase):
    def __init__(self):
        self.__embeddings = {}
        self.__inputParameters = {}
        super().__init__()

    def init(self):
        pass
    
    @property        
    def parameters(self):
        return self.__inputParameters
    @parameters.setter
    def parameters(self, tr):
        self.__inputParameters = tr

    def setJSONParameters(self, jsonContent):
        self.__inputParameters = json.loads(jsonContent)
        
    def getParameterValue(self, name, default=None):
        try:
            return self.__inputParameters[name]
        except:
            return default
        
    @property
    def jsonContent(self) -> str: 
        return json.dumps(self.content, cls=NumpyEncoder)
    @jsonContent.setter
    def jsonContent(self, jsondata):
        embsLoaded = json.loads(jsondata)
        for key, value in embsLoaded.items():
            emb = embedding()
            emb.init(value[C.JST_TEXT], value[C.JST_EMBEDDINGS])
            self.__embeddings[key] = emb

    @property
    def content(self): 
        myJsonList = {}
        for key, value in self.__embeddings.items():
            myJsonList[key] = value.content
        return myJsonList
    
    @property
    def items(self):
        return self.__embeddings
    @items.setter
    def items(self, it):
        self.__embeddings = it
        
    def __getitem__(self, item):
        """ Makes the Data column accessible via [] array
            example: df['colName']
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__embeddings.__getitem__(item)
    
    @property
    def size(self):
        return len(self.__embeddings)

    def create(self, cks) -> bool:
        return False

    def save(self, filename) -> bool:
        """ Save the chunks in a file.
        Args:
            filename (_type_): JSON chunks file
        Returns:
            bool: True if ok
        """
        try:
            self.logInfo("Save the embeddings into {}".format(filename))
            with open(filename, "w", encoding=C.ENCODING) as f:
                f.write(self.jsonContent)
            self.logInfo("Embeddings saved successfully in {}".format(filename))
            return True
        except Exception as e:
            self.logError("Impossible to open {}, error: {}".format(filename), e)
            return False

    def load(self, filename = "", content = "") -> bool:
        """ Load and build a chunk file (can be loaded from a json file or a json content). 
            Format required : Content = {"chunks": [..., ...] }
        Args:
            filename (str, optional): JSON embeddings file. Defaults to "".
            content (str, optional): JSON embeddings content. Defaults to "".
        Returns:
            bool: True if ok
        """
        try:
            self.logInfo("Load the embeddings {}".format(filename))
            if (len(filename) > 0):
                with open(filename, "r", encoding=C.ENCODING) as f:
                    self.jsonContent = f.read()
            elif (len(content) >0):
                self.jsonContent = content
                self.logInfo("Embeddings loaded successfully in {}".format(filename))
            else:
                raise Exception("There is no content in the file.")
            return True
        except Exception as e:
            self.logError("Impossible to load the embeddings file {}, error: {}".format(filename), e)
            return False