__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from src.smartgenai.connectors.documents.simplePdf import simplePdf
from src.smartgenai.connectors.documents.txt import txt
from smartgenai.framework.sets.prompt import prompt
from smartgenai.utils.trace import trace
from src.smartgenai.framework.embeddings.embeddingsBaseObject import embeddingsBaseObject
from smartgenai.framework.sets.chunks import chunks
from smartgenai.framework.sets.nearest import nearest
from smartgenai.framework.llms.LLMFactory import LLMFactory
from smartgenai.framework.embeddings.embeddingsFactory import embeddingsFactory
from smartgenai.framework.vstore.vstoreFactory import vstoreFactory
from smartgenai.framework.documents.documentFactory import documentFactory
import json
import smartgenai.utils.CONST as C

class ragWrapper():
    def __init__(self):
        self.__trace = trace()
        self.__trace.start()

    def __fmtMsgForLog(self, message, limit = C.TRACE_MSG_LENGTH):
        """ Format a message for logging
        Args:
            message (str): log message
            limit (int, optional): message max length. Defaults to C.TRACE_MSG_LENGTH.
        Returns:
            formatted message: _description_
        """
        logMsg = message.replace("\n", " ")
        dots = ""
        if (len(message) > limit):
            dots = " ..."
        logMsg = logMsg[:limit] + dots
        return logMsg

    @property
    def trace(self):
        return self.__trace

    def addMilestone(self, name, description, *others):
        self.trace.add(name, description, others)
        self.trace.addlog(C.LOGINFO, "Step {} -> {}".format(name, self.__fmtMsgForLog(description)))

    def readTXT(self, txtfile):
        """ Reads a txt file
        Args:
            txtfile (str): text file path
        Returns:
            str: text read
        """
        try:
            # Read and parse a pdf file
            self.trace.addlog(C.LOGINFO, "Read TXT file {} by using mode ...".format(txtfile))
            document = txt()
            document.trace = self.trace
            document.filename = txtfile
            document.load()
            if (len(document.content) <= 0):
                raise Exception("Error while reading the TXT document")
            self.addMilestone("PDF2TXT", "TXT file successfully loaded. Text length : {}".format(len(document.content)))
            return document
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while reading the TXT file: {}".format(str(e)))
            return txt()

    def read(self, iddocument, jsonConfig):
        """ Reads a pdf file and converts it to Text
        Args:
            idDocument (str): filename or URL
            jsonConfig (config in JSON): Type of conversion...
        Returns:
            str: text converted
        """
        try:
            # Read and parse a pdf file
            document = documentFactory.getInstance(jsonConfig)
            document.trace = self.trace
            if (document == None):
                raise Exception("The document manager has not been initiated properly")
            self.trace.addlog(C.LOGINFO, "Read document {}".format(iddocument))
            document.id = iddocument
            document.load()
            if (len(document.content) <= 0):
                raise Exception("Error while converting the PDF document to text")
            self.addMilestone("PDF2TXT", "PDF converted to TEXT successfully. Text length : {}".format(len(document.content)))
            return document
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while reading the PDF file: {}".format(str(e)))
            return simplePdf()
    
    def chunk(self, document, jsonConfig) -> chunks:
        """ Document character chunking process
        Args:
            document (elements.document): Text / document to chunk
            jsonConfig (json): configuration
        Returns:
            chunks: chunks object
        """
        try:
            document.trace = self.trace
            self.trace.addlog(C.LOGINFO, "Chunking document processing ...")
            jparams = json.loads(jsonConfig)
            method = jparams["method"]
            if (method == "character"):
                cks =  document.characterChunk(jparams["separator"], 
                                          jparams["size"], 
                                          jparams["overlap"])
            else:
                cks =  document.semanticChunk()
            if (cks == None):
                raise Exception("Error while chunking the document")
            self.addMilestone("CHUNKING","Document chunked successfully, Number of chunks : {}".format(cks.size), cks.size)
            return cks
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while chunking the document: {}".format(str(e)))
            return None
        
    def buildPrompt(self, question, nr) -> str:
        """ Build smart prompt (for RAG)
        Args:
            question (str): initial question
            nr (nearest object): list of the nearest / most similar chunks
        Returns:
            str: new prompt
        """
        try:
            self.trace.addlog(C.LOGINFO, "Building RAG prompt ...")
            myPrompt = prompt(question, nr)
            myPrompt.trace = self.trace
            customPrompt = myPrompt.build()
            if (len(customPrompt) == 0):
                raise Exception("Error while creating the prompt")
            self.addMilestone("PROMPT", "Prompt built successfully", customPrompt)
            return customPrompt
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while building the LLM prompt {}".format(str(e)))
            return ""

    def prompt(self, prompt, jsonLLMConfig):
        """ send a prompt to the LLM
        Args:
            question (str): prompt
            llmClassName (str): LLM python full path
            jsonLLMConfig (str): LLM JSON configuration
        Returns:
            str: LLM response
            str: full output
        """
        try:
            self.trace.addlog(C.LOGINFO, "Send the prompt to the LLM ...")
            llm = LLMFactory.getInstance(jsonLLMConfig)
            llm.trace = self.trace
            if (llm == None):
                raise Exception("The LLM has not been initiated properly")
            resp = llm.prompt(prompt)
            self.addMilestone("LLMPT", "LLM Reponse\n {}\n".format(resp))
            return resp, llm.jsonOutputs
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while prompting the LLM {}".format(str(e)))
            return "", 0
    
    def createEmbeddings(self, cks, jsonConfig) -> embeddingsBaseObject:
        """ create embeddings 
        Args:
            cks (chunks): Chunks object (list of texts)
            jsonConfig (json): configuration
        Returns:
            json: data and embeddings
        """
        try:
            self.trace.addlog(C.LOGINFO, "Create embeddings for list of texts/chunks ...")
            embds = embeddingsFactory.getInstance(jsonConfig)
            embds.trace = self.trace
            if (not embds.create(cks)):
                raise Exception("Error while creating the chunks embeddings")
            self.addMilestone("DOCEMBEDDGS", "Embeddings created from chunks successfully")
            return embds
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while creating the list of texts/chunks embeddings {}".format(str(e)))
            return None

    def similarityScore(self, text1, text2, vStoreJsonConfig, embdsJsonConfig):
        """ Calculate the distance (similarity) between 2 texts
        Args:
            text1 (str): text 1
            text2 (str): text 2
            vStoreJsonConfig (str): JSON with the VStore configuration
            embdsJsonConfig (str): JSON with the Embeddings configuration
        Returns:
            int: distance
        """
        try:
            self.addMilestone("OPENDS", "Open the Memory Data Store")
            vStore = vstoreFactory.getInstance(vStoreJsonConfig)
            vStore.trace = self.trace
            cks1 = chunks()
            cks1.add(text1)
            vSent1 = self.createEmbeddings(cks1, embdsJsonConfig)
            vStore.add(vSent1)
            cks2 = chunks()
            cks2.add(text2)
            vSent2 = self.createEmbeddings(cks2, embdsJsonConfig)
            similars = vStore.getNearest(vSent2, 1)
            return similars.distances[0]
        
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while performing the simirality between the 2 strings {}".format(str(e)))
            return None

    def memSimilaritySearch(self, k, textEmbeddings, listEmbeddings, jsonConfig):
        """ Makes a search in the FAISS memory and returns the k mearest datasets from the prompt
        Args:
            k (int): most k nearest chunks
            textEmbeddings (stEmbeddings): Object embeddings for the prompt
            listEmbeddings (stEmbeddings): embeddings object to add into the index
            jsonConfig (json): configuration
        Returns:
            DataFrame: List of the most nearest neighbors
        """
        try:
            self.addMilestone("OPENDS", "Open the Memory Data Store")
            vStore = vstoreFactory.getInstance(jsonConfig)
            vStore.trace = self.trace
            self.addMilestone("ADDTOVS", "Add Data/chunks to the temporary Vector store")
            vChunks = embeddingsBaseObject()
            vChunks.jsonContent = listEmbeddings
            vStore.add(vChunks)
            self.addMilestone("ADDTOVS", "Convert text embeddings")
            vText = embeddingsBaseObject()
            vText.jsonContent = textEmbeddings
            self.addMilestone("ADDTOVS", "Perform search")
            similars = vStore.getNearest(vText, k)
            self.addMilestone("VSSEARCH", "Similarity Search executed successfully")
            return similars
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while performing the similarity search {}".format(str(e)))
            return None

    def similaritySearch(self, k, embds, jsonConfig) -> nearest:
        """ Makes a search in the FAISS index and returns the k mearest datasets from the prompt

        Args:
            k (int): most k nearest chunks
            vText (stEmbeddings): Object embeddings for the prompt
            jsonConfig (json): configuration
        Returns:
            DataFrame: List of the most nearest neighbors
        """
        try:
            self.addMilestone("OPENDS", "Open the Similarity Engine Search")
            vStore = vstoreFactory.getInstance(jsonConfig)
            vStore.trace = self.trace
            self.addMilestone("ADDTOVS", "Get the vector for text")
            vText = embeddingsBaseObject()
            vText.jsonContent = embds
            self.addMilestone("ADDTOVS", "Perform search")
            similars = vStore.getNearest(vText, k)
            self.addMilestone("VSSEARCH", "Similarity Search executed successfully")
            return similars
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while performing the simirality search {}".format(str(e)))
            return None

    def storeEmbeddings(self, embds, jsonConfig) -> bool:
        """ Add text chunks (embeddings) into the Vector store engine
            Format:
            {0: {'text': 'How many jobs Joe Biden wants to create ?', 
                'embedding': array([-6.65125623e-02,  4.26685601e-01, -1.22626998e-01, -1.14275487e-02,
                                    -1.76032424e-01, -2.55425069e-02,  3.19633447e-02,  1.10126780e-02,
                                    -1.75059751e-01,  2.00320985e-02,  3.28031659e-01,  1.18581623e-01,
                                    -9.89666581e-02,  1.68430805e-01,  1.19766712e-01, -7.14423656e-02, ...] 
                },
            1: {'text': '...', 
                'embedding': array([...]
                },
            ...
            }
        Args:
            vChunks (stEmbeddings): embeddings object to add into the index
            vStore (ISimEngineWrapper): instantiated VStore object
            jsonConfig (json): configuration
        """
        try:
            self.addMilestone("ADDTOVS", "Add Data/chunks to the Vector store")
            vChunks = embeddingsBaseObject()
            vChunks.jsonContent = embds
            vStore = vstoreFactory.getInstance(jsonConfig)
            vStore.trace = self.trace
            vStore.add(vChunks)
            return True
        except Exception as e:
            self.trace.addlog(C.LOGERROR, "Error while add embeddings {}".format(str(e)))
            return False