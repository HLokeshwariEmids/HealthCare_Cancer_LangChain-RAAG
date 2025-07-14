from guardrails import Guard

# Define response guard with safety validations
response_guard = Guard.from_string("""
<guard>
    <output>
        <string name="response" min_length="5" max_length="3000" />
    </output>
    <validations>
        <validation name="no_hallucinations">
            <description>Ensure the answer avoids hallucinated medical claims.</description>
            <regex pattern="(?i)(\\bmay\\b|\\bprobably\\b|\\bmight\\b|\\bcould\\b)" match="false" />
        </validation>
        <validation name="no_sensitive_words">
            <description>Reject responses that contain sensitive terms.</description>
            <regex pattern="(?i)(suicide|kill|murder|abuse|rape)" match="false" />
        </validation>
    </validations>
</guard>
""")
