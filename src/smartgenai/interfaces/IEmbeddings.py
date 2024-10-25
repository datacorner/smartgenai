__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IEmbeddings(ABC):
    
    @property
    @abstractmethod
    def jsonContent(self):
        pass
    @jsonContent.setter
    def jsonContent(self, content):
        pass
    
    @property
    @abstractmethod
    def content(self): 
        pass
        
    @property
    @abstractmethod
    def items(self):
        pass
    @items.setter
    def items(self, it):
        pass
    
    @abstractmethod  
    def init(self):
        pass
    
    @abstractmethod
    def __getitem__(self, item):
        pass
    
    @property
    @abstractmethod
    def size(self):
        pass
    
    @abstractmethod
    def create(self, cks):
        pass
    
    @abstractmethod
    def save(self, filename):
        pass
    
    @abstractmethod
    def load(self, filename = "", content = ""):
        pass