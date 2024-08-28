__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import requests
import json
from smartgenai.framework.llms.LLMBaseObject import LLMBaseObject

# https://github.com/ollama/ollama/blob/main/docs/modelfile.md

class ollama(LLMBaseObject):

    def prompt(self, prompt)-> str:
        """ Prompt an Ollama Model
        Args:
            prompt (str): prompt to send
        Returns:
            str: LLM response
        """
        try:
            self.logInfo("Build Ollama Web Service Payload.")
            url = self.getParameterValue("url") + "/generate"
            params = {"model": self.getParameterValue("model"),
                      "prompt": prompt, 
                      "stream": False,
                      "temperature": float(self.getParameterValue("temperature")),
                      "num_ctx": int(self.getParameterValue("contextwindow"))} # num_ctx: Sets the size of the context window used to generate the next token. (Default: 2048)
            self.logInfo("Call out Ollama Web Service.")
            response = requests.post(url, json=params)
            if (response.status_code == 200):
                self.logInfo("Ollama Web Service responded successfully")
                response_text = response.text
                data = json.loads(response_text)
                # Return the number of tokens consummed
                try:
                    self.outputs["prompt_eval_count"] = data["prompt_eval_count"]
                except:
                    self.outputs["prompt_eval_count"] = 0
                self.logInfo("Number of tokens consumed {} (0 means the model does not returns the nb of tokens)".format(self.outputs["prompt_eval_count"]))
                return data["response"]
            else:
                raise Exception("Error while reaching out to the Web Service: {}", str(response.status_code, response.text))
        except Exception as e:
            self.logError("Error while calling out the Ollama Web Service, error: {}".format(str(e)))
            return str(e)