import sys
sys.path.append("./src")

import unittest

import src.smartgenai.utils.CONST as C
import json
from src.smartgenai.ragWrapper import ragWrapper
from src.smartgenai.framework.sets.chunks import chunks
from src.smartgenai.framework.documents.documentBaseObject import documentBaseObject
from src.smartgenai.framework.sets.nearest import nearest

import tests.const_test as T

class wrapper_test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.myRag = ragWrapper()
    
    def getCfg(self, filename):
        with open(filename, "r") as fichier:
            return fichier.read()
        
    def getContent(self, filename):
        with open(filename, "r", encoding=C.ENCODING) as fichier:
            return fichier.read()
        
    def setUp(self):
        print("Running Test")

    def tearDown(self):
        print("End of Test")

    def checkLog(self, log):
        jogp = json.loads(log)
        self.assertTrue(jogp["errors"] == 0)
        
    def readdoc(self, filename, config):
        response = self.myRag.read(filename, config)
        return response.content, self.myRag.trace.getFullJSON()

    def test_02_pdf2text_py(self):
        jsonCfg = self.getCfg(T.CFG_PDFPY)
        response, log = self.readdoc(T.PDFFILE, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_02_pdf2text_llp(self):
        jsonCfg = self.getCfg(T.CFG_PDFLM)
        response, log = self.readdoc(T.PDFFILE, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_03_html2text(self):
        jsonCfg = self.getCfg(T.CFG_HTML)
        response, log = self.readdoc("https://www.espn.com/", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_04_chunking_char(self):
        doc = documentBaseObject()
        doc.content = self.getContent(T.TXTFILE)
        jsonCfg = self.getCfg(T.CFG_CCHUNK)
        cks = self.myRag.chunk(doc, jsonCfg)
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(cks.jsonContent) > 0)

    def test_05_chunking_sem(self):
        doc = documentBaseObject()
        doc.content = self.getContent(T.TXTFILE)
        jsonCfg = self.getCfg(T.CFG_SCHUNK)
        cks = self.myRag.chunk(doc, jsonCfg)
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(cks.jsonContent) > 0)

    def test_06_textEmbeddings(self):
        cks = chunks()
        cks.add(T.SIMPLEPROMPT)
        embeddings = self.myRag.createEmbeddings(cks, self.getCfg(T.CFG_EMBDS_ST))
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(embeddings.jsonContent) > 0)

    def test_07_chunksEmbeddings(self):
        cks = chunks()
        cks.jsonContent = self.getContent(T.CHUNKFILE)
        embeddings = self.myRag.createEmbeddings(cks, self.getCfg(T.CFG_EMBDS_ST))
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(embeddings.jsonContent) > 0)

    def test_08_FAISS_Store(self):
        content = self.getContent(T.CHKEMBFILE)
        jsonCfg = self.getCfg(T.CFG_FAISS)
        myRag = ragWrapper()
        myRag.storeEmbeddings(content, jsonCfg)
        self.checkLog(myRag.trace.getFullJSON())
        self.assertTrue(len(myRag.trace.getFullJSON()) > 0)
        
    def test_09_FAISS_StoredIndex_Search(self):
        similars = self.myRag.similaritySearch(4, 
                                               self.getContent(T.PRTEMBFILE), 
                                               self.getCfg(T.CFG_FAISS))
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(similars.jsonContent) > 0)

    def test_10_FAISS_CalcSimilarity(self):
        vsCfg = self.getCfg(T.CFG_FAISS_MEM)
        embdsCfg = self.getCfg(T.CFG_EMBDS_ST)
        score = self.myRag.similarityScore("My cat is totally red", "I think my cat is magenta", vsCfg, embdsCfg)
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(score > 0)

    def test_11_FAISS_Memory_Search(self):
        vc = self.getContent(T.CHKEMBFILE)
        vp = self.getContent(T.PRTEMBFILE)
        jsonCfg = self.getCfg(T.CFG_FAISS_MEM)
        similars = self.myRag.memSimilaritySearch(5, vp, vc, jsonCfg)
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(similars.jsonContent) > 0)
        
    def test_15_Build_Prompt(self):
        nr = nearest()
        nr.jsonContent = self.getContent(T.NEARESTFILE)
        resp = self.myRag.buildPrompt(T.RAGPROMPT, nr)
        self.checkLog(self.myRag.trace.getFullJSON())
        self.assertTrue(len(resp) > 0)