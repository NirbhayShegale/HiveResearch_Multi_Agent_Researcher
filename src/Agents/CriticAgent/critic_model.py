from pydantic import BaseModel, Field, AliasChoices
from typing import Annotated

class CriticModel(BaseModel):
    approved: bool = Field(description="true if the draft is perfect, false if it needs revisions.", validation_alias=AliasChoices("approved", "approval"))
    feedback: str = Field(description="Specific feedback on what to fix (if rejected), or a short praise (if approved).")