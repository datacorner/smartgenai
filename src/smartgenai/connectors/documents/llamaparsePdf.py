__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.framework.documents.documentBaseObject import documentBaseObject
import smartgenai.utils.CONST as C
import mimetypes
import requests
import time

class llamaparsePdf(documentBaseObject):
    def __init__(self):
        self.__extractType = "markdown"
        super().__init__()
    
    @property
    def extractType(self):
        return self.__extractType
    @extractType.setter
    def extractType(self, q):
        self.__extractType = q
        
    def load(self):
        """ Read a pdf file and add the content as text by using llamaparse
            the LLAMAINDEX_API_KEY environment variable must be set to the API Key
            Cf.
                Login : https://cloud.llamaindex.ai/login
                Docs : https://docs.llamaindex.ai/
                Post : https://medium.com/llamaindex-blog/introducing-llamacloud-and-llamaparse-af8cedf9006b
                Example : https://github.com/allthingsllm/llama_parse/blob/main/examples/demo_api.ipynb
        Args:
            extractType (str): Extraction type text or markdown (default)
        Returns:
            bool: True if no errors
        """
        # Get the LLamaIndex Key from the LLAMAINDEX_API_KEY environment variable
        try:
            self.logInfo("Read a pdf file and add the content as text by using llamaparse.")
            if (self.id == None):
                raise Exception("A filename must me specified")
            try:
                self.logInfo("Get the llamaindex key ...")
                llamaIndexKey = self.getParameterValue("llamaindex-key", self.getEnvValue(C.LLAMAINDEX_API_KEY))
            except:
                raise Exception ("The {} environment variable or the llamaIndex Key needs to be set to use llamaparse.".format(C.LLAMAINDEX_API_KEY))
            # Upload the file
            headers = {"Authorization": f"Bearer {llamaIndexKey}", "accept": "application/json"}
            
            self.logInfo("Open the PDF file.")
            with open(self.id, "rb") as f:
                mime_type = mimetypes.guess_type(self.id)[0]
                files = {"file": (f.name, f, mime_type)}
                # send the request, upload the file
                self.logInfo("Updload the file to llamaparse.")
                url_upload = f"{C.LLAMAPARSE_API_URL}/upload"
                response = requests.post(url_upload, headers=headers, files=files)
                self.logInfo("Response Status Code: {}".format(response.status_code))
            response.raise_for_status()
            
            job_id = response.json()["id"]
            self.logInfo("Get the job id: {}".format(job_id))
            url_result = f"{C.LLAMAPARSE_API_URL}/job/{job_id}/result/{ self.extractType }"
            
            self.logInfo("Check for the result until its ready ...")
            iteration = 1
            while True:
                response = requests.get(url_result, headers=headers)
                if response.status_code == 200:
                    self.logInfo("Result is now ready.")
                    break
                time.sleep(C.LLAMAPARSE_API_WAITSEC)
                if (iteration >= C.LLAMAPARSE_ITERATION_MAX):
                    raise Exception ("Llamaindex seems not responsive or not responsive enough, please retry again.")
                iteration += 1
            self.logInfo("Download the result.")
            result = response.json()
            self.content = result[self.extractType]
        except Exception as e:
            self.logError("Error while using llamaparse : {}".format(e))
            self.content = ""
            raise