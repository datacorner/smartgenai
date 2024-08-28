__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import requests
import smartgenai.utils.CONST as C
from smartgenai.framework.llms.LLMBaseObject import LLMBaseObject
import json

class huggingFace(LLMBaseObject):

    def prompt(self, prompt) -> str:
        """ Prompt a Hugging Face model
            Cf. https://huggingface.co/docs/api-inference/detailed_parameters
            Note: the env variable C.HUGGINGFACE_API_KEY must be set with the HF key
        Args:
            prompt (str): prompt
        Returns:
            str: prompt response
        """
        try:
            self.logInfo("Get the API Hugging Face key first")
            huggingFaceKey = self.getParameterValue("huggingface_key", self.getEnvValue(C.HUGGINGFACE_API_KEY))

            self.logInfo("Build the web service payload")
            headers = {"Authorization": "Bearer " + huggingFaceKey}
            params = None
            payload = { "inputs": prompt }
            try:
                temperature = self.parameters["temperature"]
            except:
                temperature = None
            if (temperature != None):
                params = { "temperature": float(temperature) }
            if (params != None):
                payload = { "inputs": prompt , "parameters": params }
            
            # May need some time to load the model especially the first time
            self.logInfo("Call out the REST web Service {}".format(C.HUGGING_FACE_MODELS_URL + "/" + self.parameters["model"]))
            response = requests.post(C.HUGGING_FACE_MODELS_URL + "/" + self.parameters["model"], 
                                        headers=headers, 
                                        json=payload)
            if response.status_code == 200: # Response sent OK
                self.logInfo("Hugging Face responded") 
            elif response.status_code == 503: # Model currently loading (see https://huggingface.co/docs/api-inference/detailed_parameters?code=python)
                options = {}
                options["wait_for_model"] = True
                payload["options"] = options
                self.logInfo("Call out again the REST web Service with a new payload (no wait) {}".format(C.HUGGING_FACE_MODELS_URL + "/" + self.parameters["model"]))
                response = requests.post(C.HUGGING_FACE_MODELS_URL + "/" + self.parameters["model"], 
                                            headers=headers, 
                                            json=payload)
                if response.status_code != 200: # Response sent Not OK
                    raise Exception (json.dumps(json.loads(response.content)))
            else: # error !
                self.logInfo("Error while loading the model, HTTP error: {}".format(response.status_code))
                raise Exception (json.dumps(json.loads(response.content)))

            self.logInfo("Hugging Face Returned a response")
            return json.dumps(json.loads(response.content))
        except Exception as e:
            self.logError("Error while prompting the HF model {}".format(str(e)))
            return None
            