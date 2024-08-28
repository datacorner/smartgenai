__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import boto3
import json
from smartgenai.framework.llms.LLMBaseObject import LLMBaseObject

# https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-runtime_code_examples.html

class AWSBaseModel(LLMBaseObject):

    def __init__(self):
        self.__client = None
        super().__init__()
        
    def prompt(self, prompt) -> str:
        """ Prompt an AWS Bedrock Model
            need to set those 2 env variables:
                os.environ["AWS_ACCESS_KEY_ID"] = ...
                os.environ["AWS_SECRET_ACCESS_KEY"] = ...
        Args:
            prompt (str): prompt to send
        Returns:
            str: LLM response
        """
        try:
            if (self.__client == None):
                aws_access_key_id = self.getParameterValue("aws_access_key_id", self.getEnvValue("AWS_ACCESS_KEY_ID"))
                aws_secret_access_key = self.getParameterValue("aws_secret_access_key", self.getEnvValue("AWS_SECRET_ACCESS_KEY"))
                self.__client = boto3.client(service_name="bedrock-runtime", 
                                            region_name=self.getParameterValue("region"),
                                            aws_access_key_id=aws_access_key_id,
                                            aws_secret_access_key=aws_secret_access_key)

            # Convert the native request to JSON.
            request = json.dumps(self.setNativeRequest(prompt=prompt))
            try:
                # Invoke the model with the request.
                response = self.__client.invoke_model(modelId=self.getParameterValue("model"), body=request)
            except Exception as e:
                self.logInfo(f"Can't invoke '{self.getParameterValue('model')}'. Reason: { e.response['Error']['Message'] }")
                raise
            # Decode the response body.
            body = response["body"].read()
            model_response = json.loads(body)
            # Extract and sent back the response text.
            self.setCustomOutputs(model_response)
            return self.getLLMResponse(model_response)
        
        except Exception as e:
            self.logError("Error while calling out the AWS Bedrock LLM Web Service, error: {}".format(str(e)))
            return str(e)