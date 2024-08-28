__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"


from smartgenai.interfaces.ILLM import ILLM
from smartgenai.framework.objectBase import objectBase
import json

class LLMBaseObject(ILLM, objectBase):
    def __init__(self):
        self.__inputParameters = {}
        self.__outputs = {}
        super().__init__()

    def init(self):
        pass
    
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
        
    @property        
    def outputs(self):
        return self.__outputs
    
    @property        
    def jsonOutputs(self):
        return json.dumps(self.__outputs)
    
    def setCustomOutputs(self, model_response):
        pass