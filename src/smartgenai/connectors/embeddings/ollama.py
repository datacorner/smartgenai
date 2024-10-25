__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import requests
import json

import smartgenai.utils.CONST as C
from src.smartgenai.framework.embeddings.embeddingsBaseObject import embeddingsBaseObject
from smartgenai.framework.embeddings.embedding import embedding

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

class ollama(embeddingsBaseObject):
    def __init__(self):
        self.__embeddingsModel = C.OLLAMA_DEFAULT_EMB
        self.__urlbase = C.OLLAMA_LOCAL_URL
        super().__init__()

    @property
    def model(self) -> str: 
        return self.__embeddingsModel
    @model.setter
    def model(self, model):
        self.__embeddingsModel = model

    @property
    def urlbase(self) -> str: 
        return self.__urlbase
    @urlbase.setter
    def urlbase(self, url):
        self.__urlbase = url

    def __getEmbeddings(self, prompt) -> embedding:
        try:
            self.logInfo("Build the embeddings with Ollama, call the web service with the Ollama Model {}".format(self.model))
            url = self.urlbase + "/embeddings"
            params = {"model": self.model,
                      "prompt": prompt}
            response = requests.post(url, json=params)
            if (response.status_code == 200):
                response_text = response.text
                data = json.loads(response_text)
                emb = embedding()
                emb.init(prompt, data["embedding"])
                self.logInfo("Embeddings built sucessfully")
                return emb
            else:
                raise Exception("Error while reaching out to the Web Service: {}", str(response.status_code, response.text))
        except Exception as e:
            self.logError("Error while building the embeddings with Ollama, error: {}".format(e))
            return None

    def create(self, cks) -> bool:
        """ to surcharge with the embeddings class
        Args:
            cks (array []): list of chunks to create embeddings for each  
        Returns:
            numpy.ndarray: vector embeddings
        """
        try:
            self.logInfo("Create the embeddings with Ollama, {} vector will be created.".format(len(cks.items)))
            self.items = {}
            for i, item in enumerate(cks.items):
                vect = self.__getEmbeddings(item) # cks.items[0]
                self.items[str(i)] = vect
            self.logInfo("List of Embeddings created sucessfully")
        except Exception as e:
            self.logError("Error while creating the embeddings with Ollama, error: {}".format(e))
            return False