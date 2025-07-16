from guardrails import Guard
from pydantic import BaseModel

class ResponseSchema(BaseModel):
    response: str

# Define validations using XML + schema binding
response_guard = Guard.from_string(
    """
    <guard>
        <output>
            <pydantic class="ResponseSchema"/>
        </output>
        <validations>
            <validation name="no_hallucinations">
                <description>Prevent vague or speculative responses</description>
                <regex pattern="(?i)(\\bmay\\b|\\bmight\\b|\\bprobably\\b|\\bcould\\b)" match="false" />
            </validation>
            <validation name="no_sensitive_words">
                <description>Reject responses that contain sensitive terms</description>
                <regex pattern="(?i)(suicide|kill|murder|abuse|rape|die|death)" match="false" />
            </validation>
        </validations>
    </guard>
    """,
    schema_globals={"ResponseSchema": ResponseSchema}
)
