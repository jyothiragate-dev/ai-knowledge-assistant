from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """
    Request body received from the client.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question to ask the knowledge base"
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str):
        """
        Remove surrounding whitespace and reject blank questions.
        """

        value = value.strip()

        if not value:
            raise ValueError("Query cannot be empty")

        return value


class Source(BaseModel):
    """
    Source document information for the answer.
    """

    source: str
    page: str | None = None


class QueryResponse(BaseModel):
    """
    Response returned after running the RAG pipeline.
    """

    answer: str
    sources: list[Source]