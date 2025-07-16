from pydantic import BaseModel, Field, validator
import re

class SafeAnswer(BaseModel):
    response: str = Field(..., min_length=5, max_length=3000)

    @validator("response")
    def no_hallucinations(cls, v):
        if re.search(r"\bmay\b|\bprobably\b|\bmight\b|\bcould\b", v, re.IGNORECASE):
            raise ValueError("Avoid vague or speculative responses.")
        return v

    @validator("response")
    def no_sensitive_words(cls, v):
        if re.search(r"suicide|kill|murder|abuse|rape", v, re.IGNORECASE):
            raise ValueError("Avoid unsafe or sensitive terms.")
        return v
