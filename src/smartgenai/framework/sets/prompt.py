__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import smartgenai.utils.CONST as C
from smartgenai.interfaces.IPrompt import IPrompt
from jinja2 import Template
from smartgenai.framework.objectBase import objectBase

class prompt(IPrompt, objectBase):
    def __init__(self, question, similarItems):
        self.__question = question
        self.__similarItems = similarItems  # list (nearest)
        self.__template = C.PROMPT_RAG_JINJA_TEMPLATE
        super().__init__()
        
    @property
    def template(self):
        return self.__template
    @template.setter
    def template(self, t):
        self.__template = t
        
    @property
    def question(self):
        return self.__question
    @question.setter
    def question(self, q):
        self.__question = q
    
    @property
    def similarItems(self):
        return self.__similarItems
    @similarItems.setter
    def similarItems(self, q):
        self.__similarItems = q

    def loadTemplate(self, filename):
        try:
            with open(filename, "r", encoding=C.ENCODING) as f:
                self.__template = f.read()
            return True
        except Exception as e:
            return False

    def build(self):
        try:
            self.logInfo("Build the RAG prompt.")
            if (len(self.template) == 0):
                raise Exception ("A JINJA2 template must be specified.")
            if (len(self.question) == 0):
                raise Exception ("The RAG question for the prompt must be filled out.")
            if (self.similarItems.size == 0):
                raise Exception ("The number of context informations (chunks) cannot be empty.")
            j2_template = Template(self.template)
            data = { C.TPL_QUESTION: self.question, 
                     C.TPL_NEAREST: self.similarItems }
            ragPrompt = j2_template.render(data)
            self.logInfo("RAG prompt built successfully.")
            return ragPrompt
        except Exception as e:
            self.logError("Error while building the prompt: {}".format(e))
            raise