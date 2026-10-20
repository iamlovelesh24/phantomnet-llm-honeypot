# PhantomNet - Member 1 LLM Documentation

## 1. Module Ownership

Member 1 is responsible for:
- Ollama local LLM setup
- Fictional company lore
- Prompt engineering
- LLM generation interface
- Safety guardrails
- LLM evaluation and latency measurement

## 2. Local LLM

Model:
- Qwen2.5 7B
- Ollama
- Local execution

The model is used only inside the controlled PhantomNet deception environment.

## 3. Fictional Company Lore

Company:
NexusCore Technologies

Departments:
- Engineering
- Finance
- Human Resources
- IT Security
- Operations
- Executive Office

Known executives:
- Maya Chen - CEO
- Daniel Brooks - CTO
- Priya Raman - CFO
- Marcus Reed - COO

Known projects:
- Atlas - Enterprise workflow modernization
- Orion - Cloud infrastructure migration
- Sentinel - Internal security monitoring platform

## 4. LLM Interface

Main interface:

llm/model.py

The generate() function provides a common interface for other PhantomNet modules to request locally generated synthetic content.

Input:
- User/content prompt
- Optional system prompt

Output:
- Generated synthetic text
- Safety message when a prohibited request is detected

## 5. Prompt Architecture

Prompt definitions are stored in:

llm/prompts.py

The system prompt establishes:
- NexusCore fictional universe
- Approved employees
- Approved projects
- Approved project IDs
- Corporate terminology
- Consistency rules
- Synthetic-data restrictions

Specialized templates are provided for:
- Filesystem content
- SQL content
- Corporate content

## 6. Safety Guardrails

Safety logic is implemented in:

llm/guardrails.py

The guardrails:
- Block requests for real employee information
- Block requests for real credentials
- Block production credential requests
- Restrict generated content to the synthetic PhantomNet environment

No real employee, customer, credential, or production data should be used.

## 7. Evaluation

Evaluation script:

evaluation/run_llm_tests.py

Evaluation areas:
- Realism
- Response quality
- Project consistency
- Safety
- Latency

Evaluation configuration:

evaluation/llm_tests.json

## 8. Evaluation Results

Observed generation latency:

- Project Atlas realism: approximately 29.32 seconds
- Project Atlas consistency: approximately 32.35 seconds
- Project Orion consistency: approximately 29.73 seconds
- Project Sentinel consistency: approximately 27.20 seconds
- Prohibited request: approximately 0.01 seconds

The current implementation does NOT meet the project's 500 ms generation target.

The latency result is documented as a current limitation rather than claiming the target has been achieved.

## 9. Consistency Results

Project IDs were generated consistently:

- Atlas -> NC-PRJ-0001
- Orion -> NC-PRJ-0002
- Sentinel -> NC-PRJ-0003

Known executive and employee references were generally consistent.

However, evaluation identified an important limitation: the model generated an employee not present in the approved lore (Emily Thompson / NC-EMP-0005).

Therefore, lore consistency is improved but not yet perfect.

## 10. Current Limitations

1. Local LLM generation latency is significantly above the 500 ms target.
2. Prompt-level consistency does not completely prevent hallucinated employee information.
3. Additional output validation can be added in a future iteration.

## 11. Safety Boundary

PhantomNet must use synthetic fictional data only.

The system is intended for an authorized, isolated deception/lab environment and must not use real corporate, employee, customer, credential, or production information.

## 12. Handoff

Member 1 provides the following interfaces/components for integration:

- llm/model.py
- llm/prompts.py
- llm/lore.py
- llm/guardrails.py
- evaluation/run_llm_tests.py
- evaluation/llm_tests.json

Other PhantomNet modules can use generate() as the common LLM interface.

