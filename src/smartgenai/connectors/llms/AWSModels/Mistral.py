__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.connectors.llms.AWSBaseModel import AWSBaseModel

# https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-runtime_code_examples.html

class Mistral(AWSBaseModel):
    def setNativeRequest(self, prompt):
        # Format the request payload using the model's native structure.
        self.logInfo("Build AWS LLM Web Service Payload.")
        return {
                    "prompt": prompt,
                    "max_tokens": int(self.parameters["maxtokens"]),
                    "temperature": float(self.parameters["temperature"])
                }

    def getLLMResponse(self, model_response):
        return model_response["outputs"][0]["text"]