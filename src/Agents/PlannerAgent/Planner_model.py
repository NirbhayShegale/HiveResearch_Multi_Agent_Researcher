from pydantic import BaseModel, Field
from typing import Literal, Optional

class SubTask(BaseModel):
    id: int
    question: str = Field(min_length=10, max_length=500)
    aspect: str = Field(min_length=2, max_length=50)
    source_type: Literal[
        "academic", "news", "technical_docs",
        "statistics", "comparative", "opinion",
        "legal_docs", "government", "general"
    ]

class PlannerModel(BaseModel):
    original_question: str = Field(description="The user's original research question, repeated verbatim")
    sub_tasks: list[SubTask] = Field(min_length=1, max_length=2)
