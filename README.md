
# PhantomNet: Generative Cyber-Deception


An LLM-powered honeypot and cyber-deception environment developed as part of the Infotact Solutions Generative AI internship.


PhantomNet combines a locally hosted Large Language Model (LLM), a fictional corporate environment, and a generative deception filesystem to create realistic synthetic content for controlled cybersecurity research and evaluation.


## 1. Project Overview


PhantomNet simulates a fictional organization called NexusCore.


The system includes:

\- Local LLM-based response generation.

\- Fictional corporate lore and structured context.

\- Context-aware prompt engineering.

\- Input and output safety guardrails.

\- Generative virtual filesystem.

\- Synthetic files and deception scenarios.

\- Prompt consistency and filesystem safety evaluation.


## 2. Technology Stack


| Component | Technology |

|---|---|

| Language | Python |

| LLM | Qwen2.5 7B |

| Runtime | Ollama |

| Filesystem | FUSE |

| Testing | pytest |

| Version Control | Git and GitHub |


## 3. System Architecture


### Member 1 Ã¢â‚¬â€œ LLM Integration


\- Local Ollama and Qwen2.5 7B integration.

\- NexusCore fictional company lore.

\- System and content prompt engineering.

\- Context-aware response generation.

\- Input and output safety guardrails.

\- Prompt consistency evaluation.

\- LLM testing and evaluation.


### Member 2 Ã¢â‚¬â€œ Generative FUSE Filesystem


\- Generative virtual filesystem.

\- Synthetic file and directory generation.

\- Path validation and sandbox protection.

\- Read-only deception filesystem.

\- Deception scenarios.

\- Filesystem testing and benchmarking.

\- Windows compatibility.


## 4. Repository Structure


```text

PhantomNet/

Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ llm/

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ context.py

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ guardrails.py

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ lore.py

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ model.py

Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ prompts.py

Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ deception/

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ file\_generator.py

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ fuse\_fs.py

Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ path\_guard.py

Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ scenarios.py

Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ evaluation/

Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ tests/

Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ docs/

Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ README.md

Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ .gitignore

```


## 5. Setup and Installation


### Prerequisites


\- Python 3.10 or later.

\- Ollama installed.

\- Git.

\- Qwen2.5 7B model.


### Clone the repository


```bash

git clone https://github.com/iamlovelesh24/phantomnet-llm-honeypot.git

cd phantomnet-llm-honeypot

```


### Create a virtual environment


```bash

python -m venv venv

```


Windows activation:


```powershell

.\\venv\\Scripts\\Activate.ps1

```


### Install dependencies


Install the required Python packages and FUSE binding for your operating system.


### Download the model


```bash

ollama pull qwen2.5:7b

```


Ensure Ollama is running before starting LLM evaluations.


## 6. Running and Testing


### Run prompt consistency evaluation


```bash

python -m evaluation.prompt\_consistency

```


### Run the complete test suite


```bash

python -m pytest -v

```


### Run individual tests


```bash

python -m pytest tests/test\_guardrails.py -v

python -m pytest tests/test\_path\_guard.py -v

python -m pytest tests/test\_fuse\_fs.py -v

python -m pytest tests/test\_file\_generator\_validation.py -v

```


## 7. Safety and Security


### LLM Safety


\- Input validation.

\- Output validation.

\- Rejection of prohibited requests.

\- Standard safety responses for invalid content.


### Filesystem Safety


\- Sandbox-restricted filesystem access.

\- Parent-directory traversal protection.

\- Path validation.

\- Read-only deception filesystem behavior.


## 8. Evaluation


PhantomNet includes:

\- Prompt consistency evaluation.

\- Employee and project identity validation.

\- Input and output safety testing.

\- Filesystem path traversal testing.

\- Synthetic file generation validation.

\- FUSE filesystem testing.

\- Filesystem performance benchmarking.


## 9. Project Status


Implementation, integration, testing, and documentation activities for Weeks 1Ã¢â‚¬â€œ4 have been completed.


The full automated test suite passed 88 tests, and the final prompt consistency evaluation passed.


## 10. Contributors


Developed as part of the Infotact Solutions Generative AI Internship.


\- Member 1: LLM Integration and Evaluation.

\- Member 2: Generative FUSE Filesystem and Deception Shell.


## 11. Disclaimer


PhantomNet is an experimental cyber-deception project intended for controlled research, learning, and testing.


It uses fictional organizational data and synthetic content. It is not intended to access, expose, or interact with real credentials, private records, or production systems.
