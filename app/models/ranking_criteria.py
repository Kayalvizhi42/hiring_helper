from pydantic import BaseModel

class RankingCriteria(BaseModel):
    criteria: list[str]