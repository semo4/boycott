from pydantic import BaseModel,  validator
from fastapi import UploadFile, File


class Feedback(BaseModel):
    Description: str
    Image: UploadFile = File(...)
    Boycott: bool

    @validator("Description")
    def description_length(cls, v):
        if len(v) < 5:
            raise ValueError("Description must be at least 5 characters long")
        return v

    @validator("Boycott")
    def validate_boycott(cls, v):
        if not isinstance(v, bool):
            raise ValueError("Boycott must be a boolean value")
        return v
