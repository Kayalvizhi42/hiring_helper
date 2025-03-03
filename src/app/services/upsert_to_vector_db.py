# Load resume files into embeddings
from qdrant_client.http import models
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
from qdrant_client import QdrantClient
import pandas as pd


class QdrantManager:
    def __init__(self) -> None:
        self.q_client = QdrantClient(url="http://localhost:6333")
        # Create collection for resumes if it doesn't exist
        self.collection_name = "resumes"

        if not self.q_client.collection_exists(self.collection_name):
            self.q_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # FastEmbed dimension
                    distance=models.Distance.COSINE,
                ),
            )

        # Convert resumes to embeddings using FastEmbed
        self.embedding_model = TextEmbedding()
        self.reranker = TextCrossEncoder(model_name="jinaai/jina-reranker-v2-base-multilingual")

    def upsert_resumes(self, resumes: pd.DataFrame):
        payloads = []
        ids = []
        embeddings = []

        for index, row in resumes.iterrows():
            ids.append(index)

            # Convert row to string representation for embedding
            text = str(row.to_dict())

            payloads.append({"candidate_name": row["candidate_name"], "scores": text})

            embeddings.append(list(self.embedding_model.embed([text]))[0])
        # Upload vectors with payloads to Qdrant
        self.q_client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(ids=ids, payloads=payloads, vectors=embeddings),
        )

    def filter_and_rerank_points(self, candidate_scores: pd.DataFrame, user_query: str):

        candidate_names = candidate_scores['candidate_name'].to_list()
        points, _ = self.q_client.scroll(
            collection_name="resumes",
            scroll_filter=models.Filter(
                must=[models.FieldCondition(key="candidate_name", match=models.MatchAny(any=candidate_names))]
            ),
        )
        scores = []
        for point in points:
            scores.append(point.payload["scores"])

        new_scores = list(self.reranker.rerank(user_query, scores))  # returns scores between query and each document
        candidate_scores['ranking'] = new_scores

        print([(i, score, candidate_names[i]) for i, score in enumerate(new_scores)])

        return candidate_scores


if __name__ == "__main__":
    qdrant_manager = QdrantManager()

    df = pd.read_csv("samples/output/job_match_score.csv")

    qdrant_manager.upsert_resumes(df)

    ranking = qdrant_manager.filter_and_rerank_points(
        df, user_query="Get top candidate with machine learning skills"
    )

    print(ranking)
