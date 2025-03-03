from qdrant_client import QdrantClient
from qdrant_client.http import models

def create_qdrant_collections():
    # Initialize Qdrant client
    client = QdrantClient(url="http://localhost:6333")

    # Create collection for job descriptions
    client.recreate_collection(
        collection_name="job_descriptions",
        vectors_config=models.VectorParams(
            size=768,  # Vector size for sentence-transformer model
            distance=models.Distance.COSINE
        )
    )

    # Create collection for resumes
    client.recreate_collection(
        collection_name="resumes",
        vectors_config=models.VectorParams(
            size=768,  # Vector size for sentence-transformer model
            distance=models.Distance.COSINE
        )
    )

if __name__ == "__main__":
    create_qdrant_collections()