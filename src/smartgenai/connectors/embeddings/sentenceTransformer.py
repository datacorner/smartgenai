__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from sentence_transformers import SentenceTransformer
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

class sentenceTransformer(embeddingsBaseObject):
    def __init__(self):
        self.__embeddingsModel = C.EMBEDDING_MODEL
        super().__init__()

    @property
    def model(self) -> str: 
        return self.__embeddingsModel
    @model.setter
    def model(self, model):
        self.__embeddingsModel = model

    def create(self, cks) -> bool:
        """ Calculate the embeddings for list of chunks
        Args:
            cks (chunks):  chunks object
        Returns:
            str: json with data and embeddings for all chunks
        """
        try: 
            self.logInfo("Load the Sentence Transformer model {}".format(self.__embeddingsModel))
            encoder = SentenceTransformer(self.__embeddingsModel)
            vect = encoder.encode(cks.items)
            self.logInfo("Vector encoded successfully, create the return object")
            vectAndData = zip(cks.items, vect)
            self.items = {}
            for i, (chunk, vector) in enumerate(vectAndData):
                emb = embedding()
                emb.init(chunk, vector)
                self.items[str(i)] = emb
            self.logInfo("Vector embeddings created successfully.")
            return True
        except Exception as e:
            self.logError("Impossible to create the vector embeddings, error: {}".format(e))
            return False
