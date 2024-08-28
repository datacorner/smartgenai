__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"


from smartgenai.framework.objectBase import objectBase
from src.smartgenai.interfaces.IVStore import IVStore

import json

class vstoreBaseObject(IVStore, objectBase):
    def __init__(self):
        self.__inputParameters = {}
        super().__init__()

    @property        
    def parameters(self):
        return self.__inputParameters
    @parameters.setter
    def parameters(self, tr):
        self.__inputParameters = tr
        
    def setJSONParameters(self, jsonContent):
        self.__inputParameters = json.loads(jsonContent)
        
    def getParameterValue(self, name, default=None):
        try:
            return self.__inputParameters[name]
        except:
            return default