from rag.ingestion.pipeline import IngestionPipeline

ig_pipeline = IngestionPipeline()

def test_ingestion_return():
    assert ig_pipeline.ingest() == "Documents will be ingested !"