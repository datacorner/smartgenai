__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IDocument(ABC):
    @property
    @abstractmethod
    def content(self): 
        pass
    @content.setter
    def content(self, q):
        pass

    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def save(self, filename):
        pass