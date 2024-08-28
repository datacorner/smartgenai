__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IPrompt(ABC):

    @property
    @abstractmethod
    def question(self): 
        pass 
    @question.setter
    def question(self, q):
        pass
    
    @property
    @abstractmethod
    def template(self):
        pass
    @template.setter
    def template(self, t):
        pass
        
    @abstractmethod
    def build(self):
        pass
    
    @abstractmethod
    def loadTemplate(self, filename):
        pass