__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IRag(ABC):

    @property
    @abstractmethod
    def trace(self):
        pass
    
    @abstractmethod
    def readTXT(self, txtfile):
        pass
    
    @abstractmethod
    def readPDF(self, pdffile, method):
        pass
    
    @abstractmethod
    def charChunk(self, doc, separator, chunk_size, chunk_overlap):
        pass
    
    @abstractmethod
    def semChunk(self, doc):
        pass
    
    @abstractmethod
    def buildPrompt(self, question, nr):
        pass
    
    @abstractmethod
    def promptLLM(self, llm):
        pass
    
    @abstractmethod
    def createEmbeddings(self, cks):
        pass
    
    @abstractmethod
    def processSearch(self, k, vPrompt):
        pass
    
    @abstractmethod
    def addEmbeddings(self, vChunks):
        pass
    
    @abstractmethod
    def HallucinationDetector(self, response1, response2):
        pass