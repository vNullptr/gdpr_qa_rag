import pytest
from rag.ingestion.pipeline import IngestionPipeline, GDPRHTMLParser
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

@pytest.fixture
def pipeline():
    return IngestionPipeline("tests/fixtures/sample.html")


def test_parser_count(articles): 
    assert len(articles) == 4
    
def test_parser_metadata(articles):
    assert articles[0]["metadata"] == {"chapter": "I","chapter_title": "General provisions","section": 1,"article_title": "Subject-matter and objectives","article": 1}
    
def test_parser_new_chapter(articles):    
    ch2_article = next(a for a in articles if a["metadata"]["chapter"] == "II")
    assert ch2_article["metadata"]["section"] is None
    
def test_parser_art_title(articles):
    assert articles[0]["metadata"]["article_title"] == "Subject-matter and objectives"

def test_parser_chap_titl(articles):
    assert articles[0]["metadata"]["chapter_title"] == "General provisions"
    
def test_chunker_symbol(pipeline):
    chunks = pipeline.chunk([{"text":"This Regulation applies to the processing of \npersonal data wholly or partly by automated means.","metadata":{}}])
    
    assert len(chunks) == 1