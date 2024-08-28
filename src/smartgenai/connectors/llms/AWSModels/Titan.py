__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.connectors.llms.AWSBaseModel import AWSBaseModel

# https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-runtime_code_examples.html

class Titan(AWSBaseModel):

    def setNativeRequest(self, prompt):
        # Format the request payload using the model's native structure.
        self.logInfo("Build AWS LLM Web Service Payload.")
        return {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": int(self.parameters["maxtokens"]),
                    "temperature": float(self.parameters["temperature"]),
                },
            }

    def getLLMResponse(self, model_response):
        return model_response["results"][0]["outputText"]
    
    def setCustomOutputs(self, model_response):
        self.outputs["tokenCount"] = model_response["results"][0]["tokenCount"]