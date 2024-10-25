__author__ = "datacorner community"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from langchain.text_splitter import CharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from smartgenai.framework.sets.chunks import chunks
from smartgenai.interfaces.IDocument import IDocument
import smartgenai.utils.CONST as C
from smartgenai.framework.objectBase import objectBase
import json

class documentBaseObject(IDocument, objectBase):
    def __init__(self):
        self.__content = ""
        self.__inputParameters = {}
        self.__id = None
        super().__init__()
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, q):
        self.__id = q        
        
    @property
    def content(self): 
        return self.__content
    @content.setter
    def content(self, q):
        self.__content = q

    @property        
    def parameters(self):
        return self.__inputParameters
    @parameters.setter
    def parameters(self, tr):
        self.__inputParameters = tr
    
    def getParameterValue(self, name, default=None):
        try:
            return self.__inputParameters[name]
        except:
            return default
        
    def setJSONParameters(self, jsonContent):
        self.__inputParameters = json.loads(jsonContent)
        
    def load(self):
        pass
    
    def init(self):
        pass
    
    def save(self, filename):
        try:
            self.logInfo("Save document as a file.")
            with open(filename, "w", encoding=C.ENCODING) as f:
                f.write(self.__content)
            self.logInfo("Document saved successfully.")
            return True
        except Exception as e:
            self.logError("Error while saving the document: {}".format(e))
            return False

    def characterChunk(self, separator, chunk_size, chunk_overlap) -> chunks:
        """ Chunks the document content into several pieces/chunks and returns a json text with the chunks
            format : {'chunks': ['Transcript of ...', ...] }
            Note: Leverage character langchain to manage the chunks
        Args:
            separator (str): Chunks separator
            chunk_size (str): chunk size
            chunk_overlap (str): chunk overlap
        Returns:
            str: A JSON text which looks like this: {'chunks': ['Transcript of ...', ...] }
        """
        try: 
            self.logInfo("Character chunking...")
            text_splitter = CharacterTextSplitter(separator = separator, 
                                                chunk_size = chunk_size, 
                                                chunk_overlap = chunk_overlap, 
                                                length_function = len, 
                                                is_separator_regex = False)
            docs = text_splitter.create_documents([self.content])
            self.logInfo("Text splitted successfully.")
            cks = chunks()
            cks.setLangchainDocument(docs)
            return cks
        except Exception as e:
            self.logError("Error while chunking the text : {}".format(e))
            raise
    
    def semanticChunk(self) -> chunks:
        """ 
            Chunks the document content into several pieces/chunks and returns a json text with the chunks
            format : {'chunks': ['Transcript of ...', ...] }
            Note: Leverage semantic langchain to manage the chunks
        Returns:
            str: A JSON text which looks like this: {'chunks': ['Transcript of ...', ...] }
        """
        try: 
            self.logInfo("Semantic chunking...")
            hf_embeddings = HuggingFaceEmbeddings()
            model_name = C.SEMCHUNK_EMBEDDING_MODEL
            self.logInfo("Use the {} model on Hugging Face".format(model_name))
            model_kwargs = {'device': 'cpu'}
            encode_kwargs = {'normalize_embeddings': False}
            hf_embeddings = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs=encode_kwargs,
                    )
            text_splitter = SemanticChunker(hf_embeddings)
            docs = text_splitter.create_documents([self.content])
            self.logInfo("Semantic chunking executed successfully.")
            cks = chunks()
            cks.setLangchainDocument(docs)
            return cks
        except Exception as e:
            self.logError("Error while chunking the text : {}".format(e))
            raise
 