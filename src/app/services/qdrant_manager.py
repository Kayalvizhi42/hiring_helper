from qdrant_client.http import models
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
from qdrant_client import QdrantClient
import pandas as pd


class QdrantManager:
    """
    Manages interactions with Qdrant vector database for storing and retrieving resume embeddings.

    Uses FastEmbed for generating embeddings and a cross-encoder reranker for semantic search.
    """

    def __init__(self) -> None:
        """
        Initialize QdrantManager with vector database connection and ML models.
        Creates a collection for resumes if it doesn't already exist.
        """
        # Initialize Qdrant client
        self.q_client = QdrantClient(url="http://localhost:6333")
        self.collection_name = "resumes"

        # Create collection if it doesn't exist
        if not self.q_client.collection_exists(self.collection_name):
            self.q_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # FastEmbed embedding dimension
                    distance=models.Distance.COSINE,  # Use cosine similarity for vector comparisons
                ),
            )

        # Initialize ML models
        self.embedding_model = TextEmbedding()
        self.reranker = TextCrossEncoder(model_name="jinaai/jina-reranker-v2-base-multilingual")

    def upsert_resumes(self, resumes: pd.DataFrame):
        """
        Convert resumes to embeddings and store them in Qdrant.

        Args:
            resumes (pd.DataFrame): DataFrame containing resume data with candidate_name column
        """
        payloads = []
        ids = []
        embeddings = []

        # Process each resume
        for index, row in resumes.iterrows():
            ids.append(index)

            # Convert row to string for embedding generation
            text = str(row.to_dict())

            # Store candidate name and scores in payload
            payloads.append({"candidate_name": row["candidate_name"], "scores": text})

            # Generate embedding for the resume text
            embeddings.append(list(self.embedding_model.embed([text]))[0])

        # Batch upload vectors and metadata to Qdrant
        self.q_client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(ids=ids, payloads=payloads, vectors=embeddings),
        )

    def filter_and_rerank_points(self, candidate_scores: pd.DataFrame, user_query: str):
        """
        Filter candidates by name and rerank results based on semantic similarity to query.

        Args:
            candidate_scores (pd.DataFrame): DataFrame containing candidate scores
            user_query (str): Natural language query to rank candidates against

        Returns:
            pd.DataFrame: Original DataFrame with added ranking scores
        """
        # Get list of candidate names to filter by
        candidate_names = candidate_scores["candidate_name"].to_list()

        # Retrieve matching points from Qdrant
        points, _ = self.q_client.scroll(
            collection_name="resumes",
            scroll_filter=models.Filter(
                must=[models.FieldCondition(key="candidate_name", match=models.MatchAny(any=candidate_names))]
            ),
        )

        # Extract scores from payloads
        scores = []
        for point in points:
            scores.append(point.payload["scores"])

        # Rerank candidates using cross-encoder model
        new_scores = list(self.reranker.rerank(user_query, scores))
        candidate_scores["ranking"] = new_scores

        # Print debug info showing rankings
        print([(i, score, candidate_names[i]) for i, score in enumerate(new_scores)])

        return candidate_scores


if __name__ == "__main__":
    # Example usage
    qdrant_manager = QdrantManager()

    df = pd.read_csv("samples/output/job_match_score.csv")

    qdrant_manager.upsert_resumes(df)

    ranking = qdrant_manager.filter_and_rerank_points(df, user_query="Get top candidate with machine learning skills")

    print(ranking)
