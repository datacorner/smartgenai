import sys

sys.path.append("./src")
import unittest

from src.smartgenai.ragWrapper import ragWrapper
import tests.const_test as T

class llmPrompts_test(unittest.TestCase):
    def setUp(self):
        print("Running Test")

    def tearDown(self):
        print("End of Test")
        
    def test_01_Ollama_oneshot(self):
        myRag = ragWrapper()
        with open("working\\cfg\\ollama_cfg.json", "r") as fichier:
            jsonCfg = fichier.read()
        response, outs = myRag.prompt(T.SIMPLEPROMPT, jsonCfg)
        self.assertTrue(len(response) > 0)

    def test_02_HuggingFace_oneshot(self):
        myRag = ragWrapper()
        with open("working/cfg/huggingface.json", "r") as fichier:
            jsonCfg = fichier.read()
        response, outs = myRag.prompt(T.SIMPLEPROMPT, jsonCfg)
        self.assertTrue(len(response)>0)

    def test_02_AWSClaude_oneshot(self):
        myRag = ragWrapper()
        with open("working/cfg/awsclaude.json", "r") as fichier:
            jsonCfg = fichier.read()
        response, outs = myRag.prompt(T.SIMPLEPROMPT, jsonCfg)
        self.assertTrue(len(response)>0)

    def test_03_AWSTitan_oneshot(self):
        myRag = ragWrapper()
        with open("working/cfg/awstitan.json", "r") as fichier:
            jsonCfg = fichier.read()
        response, outs = myRag.prompt(T.SIMPLEPROMPT, jsonCfg)
        self.assertTrue(len(response)>0)

    def test_03_AWSMistral_oneshot(self):
        myRag = ragWrapper()
        with open("working/cfg/awsmistral.json", "r") as fichier:
            jsonCfg = fichier.read()
        response, outs = myRag.prompt(T.SIMPLEPROMPT, jsonCfg)
        self.assertTrue(len(response)>0)
