from rag.ingestion.pipeline import IngestionPipeline

ig_pipeline = IngestionPipeline("./documents/eu_gdpr.html")

def test_ingestion_return():
    assert ig_pipeline.ingest() == "Documents will be ingested !"