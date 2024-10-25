__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import json
import smartgenai.utils.CONST as C
import numpy as np
from numpyencoder import NumpyEncoder

class embedding():
    def __init__(self):
        self.__text= ""
        self.__vector = None
    
    def init(self, text, vector):
        self.__text= text
        self.__vector = vector
    
    @property
    def text(self) -> str: 
        return self.__text
    @text.setter
    def text(self, txt):
        self.__text = txt
        
    @property
    def vector(self) -> np.ndarray: 
        return self.__vector
    @vector.setter
    def vector(self, vct):
        self.__vector = vct
        
    def __str__(self):
        return self.jsonContent
    
    @property
    def jsonContent(self) -> str:
        return json.dumps(self.content, cls=NumpyEncoder)
    @jsonContent.setter
    def jsonContent(self, content):
        try:
            line = json.loads(content)
            self.text = line[C.JST_TEXT]
            self.vector = line[C.JST_EMBEDDINGS]
        except Exception as e:
            raise
    
    @property
    def content(self):
        """ Wrap the vector and the text in a list
        Returns:
            {}: list for a later JSON conversion
        """
        line = {}
        line[C.JST_TEXT] = self.text
        line[C.JST_EMBEDDINGS] = self.vector
        return line
    @content.setter
    def content(self, vct):
        self.text = vct[C.JST_TEXT]
        self.vector = vct[C.JST_EMBEDDINGS]