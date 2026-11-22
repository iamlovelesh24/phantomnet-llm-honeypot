

# PhantomNet - Member 1 LLM Documentation



## 1. Module Ownership



Member 1 is responsible for:



- Ollama local LLM setup

- Fictional company lore

- Prompt engineering

- Context-aware generation

- LLM generation interface

- Safety guardrails

- Prompt consistency evaluation

- LLM evaluation and latency measurement



## 2. Local LLM Setup



Model: Qwen2.5 7B

Runtime: Ollama

Execution: Local environment



The model is used inside the controlled PhantomNet cyber-deception environment to generate synthetic corporate content.



The model name is configured in:



`llm/model.py`



```python

MODEL_NAME = "qwen2.5:7b"

```



## 3. Fictional Company Lore



The fictional organization used throughout PhantomNet is:



**NexusCore Technologies**



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



Approved projects:



| Project | Project ID | Description |

|---|---|---|

| Atlas | NC-PRJ-0001 | Enterprise workflow modernization |

| Orion | NC-PRJ-0002 | Cloud infrastructure migration |

| Sentinel | NC-PRJ-0003 | Internal security monitoring platform |



Approved employee IDs:



- Maya Chen - NC-EMP-0001

- Daniel Brooks - NC-EMP-0002

- Priya Raman - NC-EMP-0003

- Marcus Reed - NC-EMP-0004



Source:



`llm/lore.py`



This module acts as the source of truth for fictional employees, projects, departments, IDs, and corporate terminology.



## 4. LLM Generation Interface



Main implementation:



`llm/model.py`



The `generate()` function provides a common interface for other PhantomNet modules to request synthetic content.



It accepts:



- `prompt`: User or content prompt.

- `system`: Optional system prompt.

- `context`: Optional structured context dictionary.



Generation workflow:



1. Validate the input prompt.

2. Reject prohibited requests using the safety guardrails.

3. Add the optional system prompt.

4. Convert structured context into a prompt block when supplied.

5. Send the messages to the local Qwen2.5 7B model through Ollama.

6. Validate the generated response.

7. Return generated content or the standard safety message.



The interface allows other PhantomNet components to use the same LLM generation function.



## 5. Prompt Architecture



Prompt definitions are maintained in:



`llm/prompts.py`



The system prompt establishes:



- NexusCore fictional universe.

- Approved employees and executives.

- Departments and projects.

- Approved employee and project IDs.

- Corporate terminology.

- Synthetic-data restrictions.

- Consistency requirements.



Specialized prompt templates include:



### SYSTEM_PROMPT



Defines the overall behaviour and strict lore consistency rules for the LLM.



### FILESYSTEM_PROMPT



Generates synthetic filesystem content based on the requested path and content type.



### SQL_PROMPT



Generates fictional PostgreSQL-style database content using approved NexusCore information.



### CORPORATE_CONTENT_PROMPT



Generates synthetic corporate content, including:



- Internal emails

- Project updates

- Employee profiles

- Incident reports

- Meeting notes

- Internal memos



The templates restrict generated information to the established fictional environment.



## 6. Context-Aware Generation



Implementation:



`llm/context.py`



The context interface provides deterministic structured context injection.



Main function:



`build_context(context)`



Features:



- Accepts an optional dictionary of contextual information.

- Sorts context keys to maintain deterministic ordering.

- Preserves supplied context values.

- Adds explicit context usage instructions.

- Prevents the model from assuming missing information.

- Uses a standard message when no additional context is provided.



When required information is unavailable, the model is instructed to respond:



"Not specified in PhantomNet lore."



The generated context block is included as an additional system message by `llm/model.py`.



This helps maintain consistency between filesystem content and the fictional environment.



## 7. Safety Guardrails



Implementation:



`llm/guardrails.py`



The guardrail module provides input and output validation.



### Input validation



`validate_input()`



Checks prompts against prohibited real-data request terms, including:



- Real employee

- Real customer

- Production credential

- Actual password

- Social security number

- Credit card number



### Output validation



`validate_output()`



Rejects empty or whitespace-only generated responses.



### Safety response



`safety_message()`



Returns the standard message:



"PhantomNet generates synthetic data only inside a controlled deception environment."



These checks provide basic safeguards for synthetic content generation. They are not a comprehensive security filter.



## 8. Prompt Consistency Evaluation



Implementation:



`evaluation/prompt_consistency.py`



The evaluation checks whether generated corporate content remains consistent with the approved NexusCore lore.



Approved projects:



- Atlas

- Orion

- Sentinel



Validation includes:



1. Rejecting unknown projects.

2. Rejecting empty or invalid model output.

3. Checking that the requested project name appears in the output.

4. Rejecting forbidden lore terms.

5. Validating employee IDs against the approved employee registry.

6. Validating project IDs against the approved project ID registry.

7. Rejecting project IDs that do not match the requested project.



The evaluation uses the approved information imported from:



- `llm/lore.py`

- `llm/prompts.py`



The script evaluates all approved projects and reports PASS or FAIL for each project.



## 9. Automated Prompt Consistency Tests



Test implementation:



`evaluation/test_prompt_consistency.py`



The automated tests use pytest.



Test coverage includes:



- Valid Atlas output.

- Empty output rejection.

- Unknown project rejection.

- Missing project name rejection.

- Forbidden lore term detection.

- Approved employee ID acceptance.

- Unapproved employee ID rejection.

- Approved project ID acceptance.

- Unapproved project ID rejection.

- Project ID mismatch detection.

- Case-insensitive employee ID validation.

- Case-insensitive project ID validation.

- Preventing LLM generation for unknown projects.



### Latest test result



Command:



`python -m pytest evaluation/test_prompt_consistency.py -v`



**Result: 23 passed in 0.93 seconds.**



No failures were reported.



## 10. General LLM Evaluation



Evaluation files:



- `evaluation/run_llm_tests.py`

- `evaluation/llm_tests.json`



Evaluation areas:



- Realism

- Response quality

- Project consistency

- Safety

- Generation latency



Observed generation latency:



- Project Atlas realism: approximately 29.32 seconds.

- Project Atlas consistency: approximately 32.35 seconds.

- Project Orion consistency: approximately 29.73 seconds.

- Project Sentinel consistency: approximately 27.20 seconds.

- Prohibited request: approximately 0.01 seconds.



The current implementation does not meet the project's 500 ms generation target.



This remains a documented performance limitation.



## 11. Current Limitations



1. Local LLM generation latency is significantly above the 500 ms target.

2. Prompt-level restrictions alone cannot guarantee perfect lore consistency.

3. Basic output validation does not detect every possible hallucination.

4. Context injection improves consistency but does not guarantee that every generated response follows the supplied information.

5. Additional validation and safety improvements remain part of future development.



## 12. Integration and Handoff



Member 1 provides the following components:



- `llm/model.py`

- `llm/prompts.py`

- `llm/lore.py`

- `llm/guardrails.py`

- `llm/context.py`

- `evaluation/run_llm_tests.py`

- `evaluation/llm_tests.json`

- `evaluation/prompt_consistency.py`



The `generate()` function acts as the common interface for other PhantomNet modules.



The context interface supports structured contextual information, while the prompt and guardrail modules help maintain the fictional environment.



## 13. Safety Boundary



PhantomNet must use synthetic fictional data only.



The system is intended for an authorized, isolated cyber-deception laboratory environment.



Real employee information, customer data, credentials, production secrets, and other real-world sensitive information must not be used.



All generated content must remain within the fictional NexusCore Technologies environment.
