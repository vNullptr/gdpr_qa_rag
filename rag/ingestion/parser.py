from bs4 import BeautifulSoup
import re
import unicodedata
import json


class GDPRHTMLParser:
    """
    Allows the parsing of the HTML GDPR Document into a list of dictionnaries containing the articles with their metadata.
    """
    def __init__(self, document: str):
        self.document = BeautifulSoup(document, features="html.parser")
        self.__articles = None
        
    @property
    def articles(self):
        """Getter for parsed articles list."""
        if self.__articles is not None:
            return self.__articles

        raise RuntimeError("GDPRHTMLParser -> call parse()")
        return None

    @staticmethod
    def __classify(text: str):
        """Classifies the text (html content) from GDPR document

        Args:
            text (str): the text to classify (html content).

        Returns:
            A tuple containing the class and the matched value of the text.
        """
        if match := re.fullmatch(r"CHAPTER\s([VIX]+)", text): 
            return ("chapter", match.group(1))
        elif match := re.fullmatch(r"Article\s([\d]+)", text): 
            return ("article", match.group(1))
        elif match := re.fullmatch(r"Section\s([\d]+)", text): 
            return ("section", match.group(1))

        return ("text", None)

    def parse(self):
        """
        Parses the loaded GDPR html document.
        """
        
        articles = []
        metadata = {
            "chapter": None,
            "chapter_title": None,
            "section": None,
            "article_title": None,
            "article": None
      }
        text = ""
        current = None
        expecting = None

        def flush():
            if current is not None:
                articles.append({"text": text, "metadata": metadata.copy()})

        for p in self.document.find_all(name=["p", "span"], class_=["oj-doc-ti", "oj-normal", "oj-ti-art", "oj-sti-art", "oj-ti-section-1", "oj-ti-section-2"]):
            inner = unicodedata.normalize("NFKC", p.get_text().strip())
            kind, val = self.__classify(inner)      
            
            if expecting is not None:
                metadata[expecting] = inner
                expecting = None
                continue
            
            if kind == "chapter":
                flush()
                text = ""
                expecting = "chapter_title"
                
                metadata["chapter"] = val
                metadata["section"] = None
                
            elif kind != "text":
                if kind == "article": 
                    flush()
                    current = val
                    text = ""
                    expecting = "article_title"
                metadata[kind] = int(val)
            
            else:
                text += inner + "\n"

        flush()
        self.__articles = articles
        
        return self
          