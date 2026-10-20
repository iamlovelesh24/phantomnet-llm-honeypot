from ollama import chat

from llm.guardrails import validate_input, validate_output, safety_message


MODEL_NAME = "qwen2.5:7b"


def generate(prompt: str, system: str | None = None) -> str:
    """
    Generate a response from the local PhantomNet LLM.

    Uses Ollama with a locally hosted Qwen2.5 7B model
    and applies PhantomNet safety guardrails.
    """

    if not validate_input(prompt):
        return safety_message()

    messages = []

    if system:
        messages.append({
            "role": "system",
            "content": system
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = chat(
        model=MODEL_NAME,
        messages=messages
    )

    content = response["message"]["content"]

    if not validate_output(content):
        return safety_message()

    return content
