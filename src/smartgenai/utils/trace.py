__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import time
from datetime import timedelta, datetime
import json
import smartgenai.utils.CONST as C

class trace:
    def __init__(self):
        self.perfCounter = None
        self.startTime = None
        self.stopTime = None
        self.traceSteps = []
        self.msHeader = {}
        self.stepIdx = 1
        self.logs = []
        self.counterErrors = 0
        
    def addlog(self, typelog, description):
        if (typelog == C.LOGERROR):
            self.counterErrors += 1
        if (C.ACTIVE_LOG_DEBUG and typelog == C.LOGDEBUG or 
            typelog == C.LOGINFO or 
            typelog == C.LOGERROR):
            self.logs.append("{} [{}] {}".format(datetime.now(), typelog, description))

    def initialize(self, args):
        for arg in args.keys():
            self.msHeader[arg] = args[arg]

    def start(self):
        if (self.perfCounter == None):
            self.perfCounter = time.perf_counter()
            self.startTime = datetime.now()

    def add(self, name, description, *others) -> bool:
        try:
            if (self.perfCounter == None):
                self.start()
            curms = {}
            curms["step"] = self.stepIdx
            curms["name"] = name
            curms["description"] = description
            curms["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            curms["stepduration"] = str(timedelta(seconds=time.perf_counter() - self.perfCounter))
            if (len(others) > 0):
                curms["details"] = others
            self.traceSteps.append(curms)
            self.stepIdx = self.stepIdx + 1
            return True
        except Exception as e:
            return False
        
    def stop(self):
        self.stopTime = datetime.now()

    def getFullJSON(self):
        fullJson = {}
        fullJson["headers"] = self.msHeader
        fullJson["steps"] = self.traceSteps
        fullJson["logs"] = self.logs
        fullJson["start"] = str(self.startTime)
        fullJson["errors"] = self.counterErrors
        self.stopTime = datetime.now() if self.stopTime == None else self.stopTime
        fullJson["stop"] = str(self.stopTime)
        fullJson["duration"] = str(self.stopTime - self.startTime)
        return json.dumps(fullJson)