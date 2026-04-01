import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)

prompt_template = PromptTemplate(
    input_variables=["code", "errors"],
    template="""
You are an expert Python code reviewer.

Analyze the given code and detected issues.

1. Explain each detected error clearly.
2. Suggest improvements.
3. Mention time complexity and space complexity.
4. Check naming conventions (PEP8).
5. Suggest best practices.

Detected Issues:
{errors}

Code:
{code}

Provide beginner-friendly explanations.
"""
)


def get_ai_suggestion(code: str, detected_errors: list):
    formatted_errors = "\n".join(
        [f"- {error['type']}: {error.get('message', '')}" for error in detected_errors]
    )

    final_prompt = prompt_template.format(
        code=code,
        errors=formatted_errors
    )

    response = model.invoke(final_prompt)
    return response.content