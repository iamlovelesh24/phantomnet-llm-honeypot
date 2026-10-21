from llm.model import generate
from llm.prompts import SYSTEM_PROMPT


def main():
    context = {
        "project": "Atlas",
        "employee_id": "NC-EMP-0002"
    }

    output = generate(
        "Write a very short internal project update using only the provided context.",
        SYSTEM_PROMPT,
        context
    )

    print("=" * 60)
    print("WEEK 2 CONTEXT INTERFACE TEST")
    print("=" * 60)
    print(output)


if __name__ == "__main__":
    main()