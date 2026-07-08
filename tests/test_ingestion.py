import pytest
from rag.ingestion.pipeline import IngestionPipeline, GDPRHTMLParser

#ig_pipeline = IngestionPipeline("./documents/eu_gdpr.html")

def test_parser_classifier():
    assert GDPRHTMLParser.classify("Article 16") == ("article", "16")
    assert GDPRHTMLParser.classify("CHAPTER III") == ("chapter", "III")
    assert GDPRHTMLParser.classify("Section 3") == ("section", "3")
    assert GDPRHTMLParser.classify("Random string") == ("text", None)
    
@pytest.fixture
def articles():
    with open("tests/fixtures/sample.html","r") as f:
        parser = GDPRHTMLParser(f.read())
        result = parser.parse()
        
        return result.articles
    
def test_parser_count(articles): 
    assert len(articles) == 4
    
def test_parser_metadata(articles):
    assert articles[0]["metadata"] == {"chapter": "I","chapter_title": "General provisions","section": 1,"article_title": "Subject-matter and objectives","article": 1}
    
def test_parser_new_chapter(articles):    
    ch2_article = next(a for a in articles if a["metadata"]["chapter"] == "II")
    assert ch2_article["metadata"]["section"] is None