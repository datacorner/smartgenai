__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod
from smartgenai.framework.sets.nearest import nearest

class IVStore:
   
    @abstractmethod
    def init():
        pass

    @property
    @abstractmethod
    def ready(self) -> bool:
        pass
    
    @abstractmethod
    def getNearest(self, vPrompt, k) -> nearest:
        pass
    
    @abstractmethod
    def add(self, item):
        pass