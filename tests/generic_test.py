import sys
sys.path.append("./src")

import unittest

from src.smartgenai.connectors.documents.html import html
import tests.const_test as T
from src.smartgenai.framework.sets.nearest import nearest
import src.smartgenai.utils.CONST as C

class generic_test(unittest.TestCase):
    def setUp(self):
        print("Running Test")

    def tearDown(self):
        print("End of Test")
        
    def getContent(self, filename):
        with open(filename, "r", encoding=C.ENCODING) as fichier:
            return fichier.read()
        
    def test_01_Read_URL(self):
        doc = html()
        doc.id = "https://www.espn.com/"
        doc.load()
        self.assertTrue(len(doc.content)>0)
        
    def test_02_rerank(self):
        content = self.getContent(T.NEARESTFILE)
        nr = nearest()
        nr.jsonContent = content
        nr.rerank(T.RAGPROMPT)