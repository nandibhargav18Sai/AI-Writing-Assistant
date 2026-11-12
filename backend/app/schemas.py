from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):

    mode: str = "generate"

    topic: str = Field(
        default="",
        min_length=0
    )

    content_type: str = Field(
        default=""
    )

    tone: str = Field(
        default=""
    )



class ImproveRequest(BaseModel):

    mode: str = "improve"

    text: str = Field(
        default="",
        min_length=0
    )

    task: str = Field(
        default=""
    )

    temperature: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0
    )



class SaveRequest(BaseModel):

    text: str = Field(
        default="",
        min_length=0
    )