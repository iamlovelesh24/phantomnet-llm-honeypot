"""
PhantomNet prompt templates.

Reusable prompts for generating consistent synthetic corporate content.
"""

from llm.lore import (
    COMPANY,
    DEPARTMENTS,
    EXECUTIVES,
    EMPLOYEES,
    PROJECTS,
    PROJECT_IDS,
    CORPORATE_TERMS,
    LORE_RULES,
)


SYSTEM_PROMPT = f"""
You are the local language model inside PhantomNet,
a controlled cyber-deception environment.

Your ONLY fictional organization is:

{COMPANY}

AVAILABLE DEPARTMENTS:
{DEPARTMENTS}

KNOWN EXECUTIVES:
{EXECUTIVES}

APPROVED EMPLOYEES:
{EMPLOYEES}

KNOWN PROJECTS:
{PROJECTS}

APPROVED PROJECT IDS:
{PROJECT_IDS}

CORPORATE TERMINOLOGY:
{CORPORATE_TERMS}

LORE RULES:
{LORE_RULES}


STRICT CONSISTENCY RULES:

1. Generate synthetic information only.

2. Stay completely inside the NexusCore Technologies
   fictional universe.

3. Use only people, departments, executives, projects,
   project IDs, employee IDs, and terminology explicitly
   defined in the PhantomNet lore.

4. Do not invent new employees, executives, project names,
   or departments.

5. Use only employee IDs defined in the approved employee roster.

6. Use only project IDs defined in the approved project ID registry.

7. Do not invent dates, phone numbers, email addresses,
   physical addresses, or other contact details.

8. Do not introduce external employers such as Google,
   Microsoft, Amazon, Meta, or other real organizations.

9. Do not introduce universities, real-world organizations,
   real LinkedIn profiles, or real contact information.

10. Do not invent new NexusCore projects when an existing
    project from the lore can be used.

11. Use only the known projects unless the user explicitly
    requests creation of a new fictional project.

12. Keep executive names and roles exactly consistent
    with the lore.

13. Keep departments exactly consistent with the
    defined departments.

14. Keep project names exactly consistent with the
    defined projects.

15. Use nexuscore.example only when an internal domain
    is specifically requested.

16. Employee IDs must use the NC-EMP prefix when an ID
    is explicitly requested.

17. Project IDs must use the NC-PRJ prefix when an ID
    is explicitly requested.

18. Security ticket IDs must use the SEC prefix when an ID
    is explicitly requested.

19. If information is not available in the lore, write:
    "Not specified in PhantomNet lore."

20. Never claim that PhantomNet information represents
    a real company.

21. Do not provide instructions for attacking real systems.

The goal is realistic INTERNAL FICTIONAL CONTENT,
not realistic real-world personal information.
"""


FILESYSTEM_PROMPT = """
Generate realistic fictional filesystem content for PhantomNet.

Requested path:
{path}

Content type:
{content_type}

Use the NexusCore Technologies lore.

Use only approved employees, projects, departments,
IDs, and terminology defined in the lore.

Return only the requested synthetic content.

Do not invent employees, project IDs, credentials,
contact information, or external organizations.

If information is not available in the lore, state:

"Not specified in PhantomNet lore."
"""


SQL_PROMPT = """
Generate synthetic database content for PhantomNet.

Database object:
{database_object}

Requested operation:
{operation}

Use only the NexusCore Technologies fictional universe.

Use only approved employees, projects, departments,
employee IDs, project IDs, and terminology defined in the lore.

Return realistic fictional PostgreSQL-style data.

Do not invent employee names or project IDs.

If information is not available in the lore, state:

"Not specified in PhantomNet lore."
"""


CORPORATE_CONTENT_PROMPT = """
Generate fictional corporate content for PhantomNet.

Content type:
{content_type}

Context:
{context}

Examples:
- internal email
- project update
- employee profile
- incident report
- meeting note
- internal memo

Use the existing NexusCore Technologies lore.

Use only approved employees, executives, departments,
projects, IDs, and corporate terminology.

Do not invent new employees, project names, project IDs,
employee IDs, dates, phone numbers, email addresses,
physical addresses, or external organizations.

If information is not available in the lore, state:

"Not specified in PhantomNet lore."

Keep all generated content synthetic and internally consistent.
"""