from pydantic import BaseModel, Field
from typing import  Literal

class SubTask(BaseModel):
    id: int
    question: str = Field(min_length=10, max_length=500)
    aspect: str = Field(min_length=2, max_length=50)
    priority: Literal["high", "medium", "low"]
    source_type: Literal[
        "academic", "news", "technical_docs",
        "statistics", "comparative", "opinion"
    ]
    search_hints: list[str] = Field(min_length=1, max_length=5)

class PlannerModel(BaseModel):
    original_question: str = Field(description="The user's original research question, repeated verbatim")
    complexity_assessment: Literal["simple", "moderate", "complex", "highly_complex"]
    sub_tasks: list[SubTask] = Field(min_length=1, max_length=8)
    coverage_check: str