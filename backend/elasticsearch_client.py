from elasticsearch import Elasticsearch
from config import settings
import logging

logger = logging.getLogger(__name__)

class ESClient:
    def __init__(self):
        self.es = None
        self.memory_index = []
        
        if settings.ELASTICSEARCH_URL:
            try:
                self.es = Elasticsearch(settings.ELASTICSEARCH_URL)
                # Test connection
                if self.es.ping():
                    logger.info("Connected to Elasticsearch successfully.")
                else:
                    logger.warning(f"Could not ping Elasticsearch at {settings.ELASTICSEARCH_URL}.")
                    self.es = None
            except Exception as e:
                logger.warning(f"Failed to connect to Elasticsearch at {settings.ELASTICSEARCH_URL}. Falling back to memory index. Error: {e}")
                self.es = None
        else:
            logger.info("ELASTICSEARCH_URL not set. Using memory fallback for document search.")

    def index_document(self, index_name: str, doc_id: str, document: dict):
        if self.es:
            self.es.index(index=index_name, id=doc_id, document=document)
        else:
            document["_id"] = doc_id
            self.memory_index.append(document)

    def search(self, index_name: str, query: str):
        if self.es:
            return self.es.search(index=index_name, q=query)
        else:
            # Simple in-memory fallback search
            results = []
            for doc in self.memory_index:
                if query.lower() in str(doc).lower():
                    results.append({"_source": doc})
            return {"hits": {"hits": results}}

es_client = ESClient()
