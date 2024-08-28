__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IChunks(ABC):
    @property
    @abstractmethod
    def items(self): 
        pass 
    @items.setter
    def items(self, q):
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
    def size(self): 
        pass
    
    @abstractmethod
    def add(self, chunk):
        pass
    
    @abstractmethod
    def save(self, filename):
        pass
    
    @abstractmethod
    def load(self, filename, content):
        pass
