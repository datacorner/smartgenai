__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import importlib
import importlib.resources
import smartgenai.utils.CONST as C
from src.smartgenai.framework.vstore.vstoreBaseObject import vstoreBaseObject
import json

class vstoreFactory():
    
    @staticmethod
    def getInstance(jsonConfig) -> vstoreBaseObject:
        """ This function dynamically instanciate the right data Class to create a dynamic object. 
            This to avoid in loading all the connectors (if any of them failed for example) when making a global import, 
            by this way only the needed import is done on the fly
            Args:
                classname (str): full classname (must inherit from the dpInstantiableObj Class)
            Returns:
                Object (dpInstantiableObj): Object
        """
        try:
            # Read the config file
            jparams = json.loads(jsonConfig)
            
            # Get the class to instantiate
            fullClassPath = jparams["pclass"]
            if (jparams["pclass"] == C.NULLSTRING):
                raise Exception("The {} parameter is mandatory and cannot be empty".format(fullClassPath))
            else:
                # Get the latest element : the class name without the path
                llmClass = fullClassPath.split(".")[-1]

            # Instantiate the object
            datasourceObject = importlib.import_module(name=fullClassPath)
            llmClassInst = getattr(datasourceObject, llmClass)
            objectInst = llmClassInst()
            
            # Add the parameters from the config json file
            objectInst.setJSONParameters(jsonConfig)
            # Initialize if necessary
            objectInst.init()
            
            return objectInst
        
        except Exception as e: 
            return None
    