__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import chromadb
from chromadb.utils import embedding_functions
import smartgenai.utils.CONST as C
import pandas as pd
from smartgenai.framework.sets.nearest import nearest
import hashlib
from src.smartgenai.framework.vstore.vstoreBaseObject import vstoreBaseObject

""" 
    Leverage Chroma DB
    Starts server locally bveforehand: 
        $ chroma run --path C:/chromadb
        
    If error, then uninstall and reinstall chromadb:
    
        python -m pip uninstall chromadb
        python -m pip uninstall chromadb-client
    then 
        python -m pip install chromadb
        python -m pip install chromadb-client
"""
embFunction = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=C.CDB_DEFAULT_EMBEDDINGSMODEL_ST)

class ChromaDB(vstoreBaseObject):
    def __init__(self):
        self.__chroma_client = None
        self.__currentCollection = None
        super().__init__()
    
    def init(self):
        self.__currentCollection = self.getParameterValue("collection", None)
        self.initServer(self.getParameterValue("host", None), 
                        self.getParameterValue("port", None))
    
    def initServer(self, host, port):
        self.__chroma_client = chromadb.HttpClient(host=host, port=port)
        
    def initLocal(self):
        self.__chroma_client = chromadb.Client()
        
    def initPersistent(self, location):
        self.__chroma_client = chromadb.PersistentClient(path=location)
    
    @property
    def ready(self) -> bool:
        return (self.__chroma_client != None)
    
    @property
    def client(self):
        return self.__chroma_client

    @property
    def currentCollection(self): 
        return self.__currentCollection
    @currentCollection.setter
    def currentCollection(self, q):
        self.__currentCollection = q

    def __getCDBCollection(self, name) -> chromadb.Collection:
        try:
            if (len(name)<=0):
                raise Exception ("A collection must be specified")
            return self.__chroma_client.get_or_create_collection(name, embedding_function=embFunction)
        except Exception as e:
            self.logError("Error while loading the collection, error={}".format(e))
            return None
        
    def __getHash(self, myText):
        return hashlib.sha256(myText.encode()).hexdigest()
        
    def add(self, vItems) -> int:
        """ Add a item list ([ str ]) in the DB
        Args:
            vItems (DataFrame): Data and embeddings
        """
        try:
            if (self.__currentCollection == None):
                raise Exception("A collection must be specified.")
            self.logInfo("Insert an new vector in the Chroma DB collection {}".format(self.__currentCollection))
            dfNewContent = pd.DataFrame(vItems.content).T
            collection = self.__getCDBCollection(self.__currentCollection)
            if (collection == None):
                raise Exception ("Impossible to get the collection from Chroma DB")
            # prepare the object to return with text and generated id
            dataInserted = {}
            dataInserted["contents"] = dfNewContent[C.JST_TEXT].tolist()
            dataInserted["ids"] = [ self.__getHash(p) for p in dfNewContent[C.JST_TEXT].tolist() ]
            # add to the cdb collection
            collection.add(documents=dataInserted["contents"],
                           embeddings=dfNewContent[C.JST_EMBEDDINGS].tolist(),
                           ids=dataInserted["ids"],
                           metadatas=[{"md_id": i} for i in range(len(dfNewContent))]) 
            self.logInfo("Vector saved successfully.")              
            return dataInserted
        except Exception as e:
            self.logError("Error while adding a new vector in the collection, error={}".format(e))
            raise
        
    def getNearest(self, vText, k):
        """ Process the similarity search on the existing Chroma DB (and the given prompt)
                --> k is set to the total number of vectors within the index
                --> ann is the approximate nearest neighbour corresponding to those distances
        Args:
            vText (json): Prompt's embeddings
            k (int): Nb of nearest to return
        Returns:
            DataFrame: List of the most nearest neighbors
        """
        try:
            if (self.__currentCollection == None):
                raise Exception("A collection must be specified.")
            self.logInfo("Perform a similarity search in the Chroma DB collection {}".format(self.__currentCollection))     
            collection = self.__getCDBCollection(self.__currentCollection) 
            if (collection == None):
                raise Exception ("Impossible to get the collection from Chroma DB")
            result = collection.query(query_embeddings=vText.content["0"]["embedding"], n_results=k)
            nr = nearest()
            nr.items = result["documents"][0]
            nr.distances = result["distances"][0]
            nr.metadatas = result["metadatas"][0]
            nr.ids = result["ids"][0]
            self.logInfo("Similarity search exectuted successfully with {} results".format(k)) 
            return nr
        except Exception as e:
            self.logError("Error while performing the similarity search in the the collection, error={}".format(e))
            raise