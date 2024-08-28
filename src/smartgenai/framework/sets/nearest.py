__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import smartgenai.utils.CONST as C
import json
from numpyencoder import NumpyEncoder
from smartgenai.interfaces.INearest import INearest
from smartgenai.framework.objectBase import objectBase
# pip install flashrank
from flashrank import Ranker, RerankRequest

""" Manages the Chunks file structure (JSON)
    Content = {"chunks": [..., ...] }
"""

class nearest(INearest, objectBase):
    def __init__(self):
        self.__items = [] # simple Array which contains all the items
        self.__distances = [] # list of distances per items
        self.__metadatas = [] # metadata to store
        self.__ids = [] # IDs
        
    @property
    def items(self): 
        return self.__items 
    @items.setter
    def items(self, q):
        self.__items = q
    def __getitem__(self, item):
        """ Makes the Data column accessible via [] array
            example: df['colName']
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__items.__getitem__(item)
    
    @property
    def distances(self): 
        return self.__distances 
    @distances.setter
    def distances(self, q):
        self.__distances = q
        
    @property
    def metadatas(self): 
        return self.__metadatas 
    @metadatas.setter
    def metadatas(self, q):
        self.__metadatas = q
        
    @property
    def ids(self): 
        return self.__ids 
    @ids.setter
    def ids(self, q):
        self.__ids = q
        
    @property
    def jsonContent(self) -> str: 
        try:
            return json.dumps(self.__createEnveloppe(), cls=NumpyEncoder)
        except:
            return "{}"
    @jsonContent.setter
    def jsonContent(self, content):
        try:
            jsonEnv = json.loads(content)
            self.__items = jsonEnv[C.JST_NEAREST]
        except Exception as e:
            self.__items = []
            raise

    @property
    def size(self) -> items: 
        return len(self.items)
    
    def __createEnveloppe(self) -> str:
        jsonEnv = {}
        jsonEnv[C.JST_NEAREST] = self.items
        return jsonEnv
    
    def add(self, item):
        self.__items.append(item)

    def save(self, filename) -> bool:
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

    def load(self, filename = "", content = "") -> bool:
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
            elif (len(content) >0):
                jsonEnv = content
            else:
                return False
            self.items = jsonEnv[C.JST_NEAREST]
            return True
        except Exception as e:
            return False
        
    def rerank(self, text) -> bool:
        try:
            passages = []
            for i in range(len(self.items)):
                passages.append({ "id": i+1, 
                                "text": self.items[i] })
                # 1) Need to put distance + metadata in the meta
                # 2) reorder everything
            ranker = Ranker()
            rerankrequest = RerankRequest(query=text, passages=passages)
            results = ranker.rerank(rerankrequest)
            print(results)
            return True
        except Exception as e:
            return False