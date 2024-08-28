import sys
sys.path.append("./src")

import unittest

import src.smartgenai.utils.CONST as C
import tests.wrappers as wp
import json

import tests.const_test as T

class wrapper_test(unittest.TestCase):
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

    def test_01_ollamaPrompt(self):
        jsonCfg = self.getCfg(T.CFG_OLLAMA)
        response, outputs, log = wp.prompt("do you know pytorch ?", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_01_huggingfacePrompt(self):
        jsonCfg = self.getCfg(T.CFG_HF)
        response, tok, log = wp.prompt("do you know pytorch ?", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_01_AWSClaudePrompt(self):
        jsonCfg = self.getCfg(T.CFG_AWSCLAUDE)
        response, tok, log = wp.prompt("do you know pytorch ?", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)
        
    def test_01_AWSMistralPrompt(self):
        jsonCfg = self.getCfg(T.CFG_AWSMISTRAL)
        response, tok, log = wp.prompt("do you know pytorch ?", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)
        
    def test_01_AWSTitanPrompt(self):
        jsonCfg = self.getCfg(T.CFG_AWSTITAN)
        response, tok, log = wp.prompt("do you know pytorch ?", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)
        
    def test_02_pdf2text_py(self):
        jsonCfg = self.getCfg(T.CFG_PDFPY)
        response, log = wp.readdoc(T.PDFFILE, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_02_pdf2text_llp(self):
        jsonCfg = self.getCfg(T.CFG_PDFLM)
        response, log = wp.readdoc(T.PDFFILE, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_03_html2text(self):
        jsonCfg = self.getCfg(T.CFG_HTML)
        response, log = wp.readdoc("https://www.espn.com/", jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_04_chunking_char(self):
        content = self.getContent(T.TXTFILE)
        jsonCfg = self.getCfg(T.CFG_CCHUNK)
        s, response, log = wp.chunking(content, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_05_chunking_sem(self):
        content = self.getContent(T.TXTFILE)
        jsonCfg = self.getCfg(T.CFG_SCHUNK)
        s, response, log = wp.chunking(content, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_06_textEmbeddings(self):
        jsonCfg = self.getCfg(T.CFG_EMBDS_ST)
        s, response, log = wp.textEmbeddings(T.SIMPLEPROMPT, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_07_chunksEmbeddings(self):
        content = self.getContent(T.CHUNKFILE)
        jsonCfg = self.getCfg(T.CFG_EMBDS_ST)
        s, response, log = wp.chunksEmbeddings(content, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_08_FAISS_Store(self):
        content = self.getContent(T.CHKEMBFILE)
        jsonCfg = self.getCfg(T.CFG_FAISS)
        log = wp.VS_Store(content, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(log) > 0)
        
    def test_09_FAISS_StoredIndex_Search(self):
        content = self.getContent(T.PRTEMBFILE)
        jsonCfg = self.getCfg(T.CFG_FAISS)
        response, log = wp.VS_Search(content, 4, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_10_FAISS_CalcSimilarity(self):
        vsCfg = self.getCfg(T.CFG_FAISS_MEM)
        embdsCfg = self.getCfg(T.CFG_EMBDS_ST)
        response, log = wp.calcSimilarity("My cat is totally red", "I think my cat is magenta", vsCfg, embdsCfg)
        self.checkLog(log)
        self.assertTrue(response > 0)

    def test_11_FAISS_Memory_Search(self):
        vc = self.getContent(T.CHKEMBFILE)
        vp = self.getContent(T.PRTEMBFILE)
        jsonCfg = self.getCfg(T.CFG_FAISS_MEM)
        response, log = wp.faissMemorySearch(5, vp, vc, jsonCfg)
        self.checkLog(log)
        self.assertTrue(len(response) > 0)

    def test_13_ChromaDB_Store(self):
        content = self.getContent(T.CHKEMBFILE)
        jsonCfg = self.getCfg(T.CFG_CHROMADB)
        log = wp.VS_Store(content, jsonCfg)
        self.checkLog(log)

    def test_14_ChromaDB_Search(self):
        content = self.getContent(T.PRTEMBFILE)
        jsonCfg = self.getCfg(T.CFG_CHROMADB)
        response, log = wp.VS_Search(content, 5, jsonCfg)
        self.checkLog(log)
        
    def test_15_Build_Prompt(self):
        content = self.getContent(T.NEARESTFILE)
        response, log = wp.buildPrompt(T.RAGPROMPT, content)
        self.checkLog(log)