"""
PhantomNet LLM context interface.

Builds deterministic, structured context blocks for the
PhantomNet local LLM so generated content remains consistent
with the supplied fictional environment.
"""

from typing import Any


def build_context(context: dict[str, Any] | None = None) -> str:
    """
    Convert structured context into a deterministic prompt block.

    Context values are preserved as supplied and formatted in a
    stable order so repeated calls produce consistent prompts.
    """

    if not context:
        return (
            "PHANTOMNET CONTEXT:\n"
            "No additional context provided.\n\n"
            "CONTEXT USAGE:\n"
            "Do not assume information that is not provided."
        )

    lines = [
        "PHANTOMNET CONTEXT:",
        "Use the following context as authoritative input for this request.",
        "",
    ]

    for key in sorted(context):
        value = context[key]
        lines.append(f"- {key}: {value}")

    lines.extend([
        "",
        "CONTEXT USAGE:",
        "1. Use the supplied context when generating the response.",
        "2. Do not replace supplied values with different values.",
        "3. Do not invent missing context.",
        '4. If required information is unavailable, state: "Not specified in PhantomNet lore."',
    ])

    return "\n".join(lines)
