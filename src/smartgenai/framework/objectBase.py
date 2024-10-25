__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import smartgenai.utils.CONST as C
import os

class objectBase():
    def __init__(self):
        self.__trace = None
        
    @property        
    def trace(self):
        return self.__trace
    @trace.setter
    def trace(self, tr):
        self.__trace = tr

    def getEnvValue(self, name, default=None):
        try:
            return os.environ[name]
        except:
            return default

    def __log(self, level, myLog):
        try:
            # in case the contructor did not called out super() ;-)
            self.__trace.addlog(level, myLog)
        except:
            pass
            
    def logInfo(self, myLog):
        if (self.__trace != None):
            self.__log(C.LOGINFO, myLog)
            
    def logError(self, myLog):
        if (self.__trace != None):
            self.__log(C.LOGERROR, myLog)