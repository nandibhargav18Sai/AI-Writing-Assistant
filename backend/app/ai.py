import os

from dotenv import load_dotenv
from groq import Groq

from app.prompts import (
    SYSTEM_PROMPT,
    BLOCKED,
    ERROR_MESSAGE
)


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def allowed(text):
    text = text.lower()

    return not any(
        word in text
        for word in BLOCKED
    )


def generate(prompt, temperature=0.5):

    if not allowed(prompt):
        return ERROR_MESSAGE

    try:

        if "quiz" in prompt.lower():
            temperature = 0.2

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            temperature=temperature,
            max_tokens=1200,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    except Exception as e:

        raise Exception(
            f"Groq API error: {str(e)}"
        )