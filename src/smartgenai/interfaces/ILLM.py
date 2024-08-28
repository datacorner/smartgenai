__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class ILLM:
   
    @abstractmethod
    def setJSONParameters(self, jsonContent):
        pass

    @abstractmethod  
    def init(self):
        pass
    
    @property   
    @abstractmethod     
    def parameters(self):
        pass
    @parameters.setter
    def parameters(self, tr):
        pass
    
    @property
    @abstractmethod
    def outputs(self):
        pass
    
    @abstractmethod
    def prompt(self, prompt) -> str:
        pass
