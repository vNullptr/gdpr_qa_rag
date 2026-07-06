from rag.query.pipeline import QueryPipeline

q_pipeline = QueryPipeline()

def test_answer_shape():
    answer = q_pipeline.query("test question")
    
    assert isinstance(answer, dict)
    assert isinstance(answer["answer"], str)
    assert isinstance(answer["citations"], list)