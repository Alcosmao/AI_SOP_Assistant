from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question about the SOP document"
    )

class AskResponse(BaseModel):
    question: str
    has_context: bool
    answer: str
    sources: str
    checklist: list[str]