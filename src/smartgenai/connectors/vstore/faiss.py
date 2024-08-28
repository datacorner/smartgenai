__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import pandas as pd
import numpy as np
import faiss # pip install faiss-cpu (https://pypi.org/project/faiss-cpu/)
import pickle
import os
import smartgenai.utils.CONST as C
from smartgenai.framework.sets.nearest import nearest
from src.smartgenai.framework.vstore.vstoreBaseObject import vstoreBaseObject

""" 
    Leverage Meta FAISS
"""
class faiss(vstoreBaseObject):
    def __init__(self):
        self.__index = None   # FAISS Index
        self.__dfContent = pd.DataFrame(columns = [C.JST_TEXT, C.JST_EMBEDDINGS]) # real data that are indexed
        super().__init__()

    @property
    def inMemorySearch(self):
        return (len(self.indexName) == 0 or len(self.indexPath) == 0)
    
    @property
    def indexName(self):
        return self.getParameterValue("name", "")
    @property
    def indexPath(self):
        return self.getParameterValue("filepath", "")
    
    def init(self):
        self.load()
        
    def save(self):
        """ Save the FAISS index and the data (chunks)
        Args:
            filepath (str, optional): _description_. Defaults to "./backup/".
            name (str, optional): _description_. Defaults to "faissbackup".
        """
        try:
            if (not self.inMemorySearch):
                self.logInfo("Save FAISS index and data.")
                datafile = os.path.join(self.indexPath, self.indexName + ".data")
                self.logInfo("Save FAISS data in file {}".format(datafile))
                indexfile = os.path.join(self.indexPath, self.indexName + ".index")
                self.logInfo("Save FAISS index in file {}".format(indexfile))
                with open(datafile, "wb") as f:
                    pickle.dump(self.__dfContent, f)
                faiss.write_index(self.__index, indexfile)
                self.logInfo("FAISS index and data saved successfully.")
        except Exception as e:
            self.logError("Impossible to save FAISS index and data saved, error= {}".format(e))
            raise

    def load(self):
        """ Read the FAISS index and the data (chunks) saved previously
        Args:
            filepath (str, optional): _description_. Defaults to "./backup/".
            name (str, optional): _description_. Defaults to "faissbackup".
        """
        try:
            if (not self.inMemorySearch):
                self.logInfo("Load FAISS index and data.")
                datafile = os.path.join(self.indexPath, self.indexName + ".data")
                self.logInfo("Load FAISS data in file {}".format(datafile))
                indexfile = os.path.join(self.indexPath, self.indexName + ".index")
                self.logInfo("Load FAISS index in file {}".format(indexfile))
                with open(datafile, "rb") as f:
                    self.__dfContent = pickle.load(f)
                self.__index = faiss.read_index(indexfile)
                self.logInfo("FAISS index and data loaded successfully.")
        except Exception as e:
            self.logError("Impossible to load FAISS index and data, error= {}".format(e))
            raise
        
    @property
    def size(self) -> int:
        return self.__index.ntotal
    
    @property
    def ready(self) -> bool:
        """check if ready for searching for the NN
        Returns:
            bool: True if index ready
        """
        try:
            return self.__index.is_trained #and not self.dfContent.empty
        except:
            return False

    def add(self, item):
        """ Index a new item
        Args:
            item (stEmbeddings): embeddings object to add into the index
        """
        try:
            self.logInfo("Add a new vector in the FAISS index.")
            # Get source data and JSON -> DF
            dfNewContent = pd.DataFrame(item.content).T
            embeddings = [ np.asarray(v) for v in dfNewContent[C.JST_EMBEDDINGS] ]
            self.__addToIndexFlatL2(embeddings)
            # Concat the content with the existing DF
            self.__dfContent = pd.concat([self.__dfContent, dfNewContent])
            self.logInfo("Vector indexed successfully.")
            self.save() # persist if not in memory
            return self.__dfContent
        except Exception as e:
            self.logError("Impossible to add a new vector in the FAISS index, error= {}".format(e))
            raise
        
    def __addToIndexFlatL2(self, embeddings):
        """
            Build a Flat L2 index
        """
        vout = self.__prepareEmbeddings(embeddings)
        self.__index = faiss.IndexFlatL2(vout.shape[1])
        self.__index.add(vout)

    def __prepareEmbeddings(self, vects):
        """ Prepare the embeddings for indexing
        Args:
            vects (array/embedding): vector
        Returns:
            array/embedding: vector prepared
        """
        vout =  np.asarray(vects)
        vout = vout.astype(np.float32) # Only support ndarray in 32 bits !
        faiss.normalize_L2(vout)
        return vout

    def getNearest(self, vPrompt, k) -> nearest:
        """ Process the similarity search on the existing FAISS index (and the given prompt)
                --> k is set to the total number of vectors within the index
                --> ann is the approximate nearest neighbour corresponding to those distances
        Args:
            prompt (json): Prompt's embeddings
            k (int): Nb of nearest to return
        Returns:
            nearest object: List of the most nearest neighbors
        """
        try: 
            self.logInfo("Perform a similarity search in the FAISS Index with k={}".format(k))
            if (not self.ready):
                raise Exception("The FAISS Index is not loaded properly.")
            self.logInfo("Get prompt vector only and normalize it ....")
            prompt = vPrompt.content
            idx = "0" if (str(type(list(prompt.keys())[0])) == "<class 'str'>") else 0
            vector = self.__prepareEmbeddings([ prompt[idx][C.JST_EMBEDDINGS] ])
            self.logInfo("Process the Similarity search ...")
            distances, ann = self.__index.search(vector, k=k)
            # Sort search results and return a DataFrame
            results = pd.DataFrame({'distances': distances[0], 
                                    'ann': ann[0]})
            self.__dfContent.index = self.__dfContent.index.astype(int)
            merge = pd.merge(results, self.__dfContent, left_on='ann', right_index=True)
            nr = nearest()
            nr.items = merge["text"].to_list()
            nr.distances = merge["distances"].to_list()
            self.logInfo("Similarity search executed successfully")
            return nr
        except Exception as e:
            self.logError("Impossible to add a new vector in the FAISS index, error= {}".format(e))
            raise