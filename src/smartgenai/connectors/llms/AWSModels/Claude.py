__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.connectors.llms.AWSBaseModel import AWSBaseModel

# https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-runtime_code_examples.html

class Claude(AWSBaseModel):

    def setNativeRequest(self, prompt):
        # Format the request payload using the model's native structure.
        self.logInfo("Build AWS LLM Web Service Payload.")
        return {
            "anthropic_version": self.parameters["version"],
            "max_tokens": int(self.parameters["maxtokens"]),
            "temperature": float(self.parameters["temperature"]),
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", 
                                "text": prompt}],
                }
            ],
        }
    
    def setCustomOutputs(self, model_response):
        self.outputs["input_tokens"] = model_response["usage"]["input_tokens"]
        self.outputs["output_tokens"] = model_response["usage"]["output_tokens"]
        
    def getLLMResponse(self, model_response):
        return model_response["content"][0]["text"]