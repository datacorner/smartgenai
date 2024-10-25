__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class INearest(ABC):

    @property
    @abstractmethod
    def items(self): 
        pass 
    @items.setter
    def items(self, q):
        pass
    
    @property
    @abstractmethod
    def ids(self): 
        pass
    @ids.setter
    def ids(self, q):
        pass
    
    @property
    @abstractmethod
    def distances(self): 
        pass 
    @distances.setter
    def distances(self, q):
        pass
    
    @property
    @abstractmethod
    def metadatas(self): 
        pass 
    @metadatas.setter
    def metadatas(self, q):
        pass
        
    @property
    @abstractmethod
    def jsonContent(self): 
        pass
    @jsonContent.setter
    def jsonContent(self, content):
        pass
    
    @property
    @abstractmethod
    def size(self) -> items: 
        pass
    
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def save(self, filename):
        pass
    
    @abstractmethod
    def load(self, filename, content):
        pass