__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import requests
import json
from smartgenai.framework.llms.LLMBaseObject import LLMBaseObject

# https://github.com/ollama/ollama/blob/main/docs/modelfile.md

class chatGPT(LLMBaseObject):

    def prompt(self, prompt)-> str:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.parameters["apikey"]}"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.parameters["temperature"]
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code}, {response.text}"
            
        except Exception as e:
            self.logError("Error while calling out the Ollama Web Service, error: {}".format(str(e)))
            return str(e)