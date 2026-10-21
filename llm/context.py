"""
PhantomNet LLM context interface.

Provides a simple context structure that can be supplied to
the LLM by other PhantomNet modules.

Context retrieval/storage is handled by the appropriate module.
This file only defines the interface used by the LLM layer.
"""

from typing import Any


def build_context(context: dict[str, Any] | None = None) -> str:
    """
    Convert structured context into a deterministic text block
    that can be supplied to the PhantomNet LLM.
    """

    if not context:
        return "No additional context provided."

    lines = ["PHANTOMNET CONTEXT:"]

    for key, value in context.items():
        lines.append(f"{key}: {value}")

    return "\n".join(lines)