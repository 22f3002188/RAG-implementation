import json
import re
import os
from langchain_openai import AzureChatOpenAI


# ==============================
# SYSTEM PROMPT
# ==============================
SYSTEM_PROMPT = """
You are a QA assistant.

ONLY use the provided context.
DO NOT invent features.
If information is missing, clearly state assumptions.

Return output STRICTLY in valid JSON with the following keys:
- Use Case Title
- Goal
- Preconditions
- Test Data
- Steps
- Expected Results
- Negative Cases
- Boundary Cases
"""


# ==============================
# AZURE OPENAI CLIENT
# ==============================

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0,
)



# ==============================
# HELPER: CLEAN + PARSE JSON
# ==============================
def extract_json(text: str) -> dict:
    """
    Removes markdown fences and parses JSON safely
    """
    # Remove ```json ``` if present
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(
            "LLM did not return valid JSON. Raw output:\n" + cleaned
        )


# ==============================
# MAIN GENERATION FUNCTION
# ==============================
def generate_test_cases(context: str, query: str) -> dict:
    prompt = f"""
Context:
{context}

User Query:
{query}
"""

    response = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    )

    # RETURN STRUCTURED JSON
    return extract_json(response.content)
