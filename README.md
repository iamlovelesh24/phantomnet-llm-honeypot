#

# \# PhantomNet: Generative Cyber-Deception

#

# An LLM-powered honeypot and cyber-deception environment developed as part of the Infotact Solutions Generative AI internship.

#

# PhantomNet combines a locally hosted Large Language Model (LLM) with a synthetic fictional corporate environment and a generative deception filesystem. Its purpose is to create realistic-looking but fictional content for controlled cybersecurity research and evaluation.

#

# \## 1. Project Overview

#

# PhantomNet uses generative AI to simulate a fictional organization called \*\*NexusCore\*\*.

#

# The system combines:

#

# \- Local LLM-based response generation.

# \- Fictional corporate lore and structured context.

# \- Context-aware prompt engineering.

# \- Input and output safety guardrails.

# \- A generative virtual filesystem.

# \- Synthetic files and deception scenarios.

# \- Prompt consistency and filesystem safety evaluation.

#

# All generated organizational information is intended to remain fictional and synthetic.

#

# \## 2. Technology Stack

#

# | Component | Technology |

# |---|---|

# | Programming language | Python |

# | LLM | Qwen2.5 7B |

# | LLM runtime | Ollama |

# | LLM integration | Ollama Python client |

# | Prompt engineering | Custom system and content prompts |

# | Context management | Python |

# | Filesystem | FUSE |

# | Testing | pytest |

# | Version control | Git and GitHub |

#

# \## 3. System Architecture

#

# PhantomNet consists of two main components.

#

# \### Member 1 – LLM Integration

#

# Responsible for:

#

# \- Local Ollama and Qwen2.5 7B integration.

# \- NexusCore fictional company lore.

# \- System and content prompt engineering.

# \- Context-aware response generation.

# \- Input and output safety guardrails.

# \- Prompt consistency evaluation.

# \- LLM testing and evaluation.

#

# \### Member 2 – Generative FUSE Filesystem

#

# Responsible for:

#

# \- Generative virtual filesystem.

# \- Synthetic file and directory generation.

# \- Path validation and sandbox protection.

# \- Read-only deception filesystem behavior.

# \- Deception scenarios.

# \- Filesystem testing and benchmarking.

# \- Windows compatibility improvements.

#

# \## 4. Repository Structure

#

# ```text

# PhantomNet/

# │

# ├── llm/

# │   ├── context.py

# │   ├── guardrails.py

# │   ├── lore.py

# │   ├── model.py

# │   └── prompts.py

# │

# ├── deception/

# │   ├── file\_generator.py

# │   ├── fuse\_fs.py

# │   ├── path\_guard.py

# │   └── scenarios.py

# │

# ├── evaluation/

# │   ├── context\_tests.py

# │   ├── llm\_tests.json

# │   ├── prompt\_consistency.py

# │   └── run\_llm\_tests.py

# │

# ├── tests/

# │   ├── benchmark\_fuse\_fs.py

# │   ├── test\_file\_generator\_validation.py

# │   ├── test\_fuse\_fs.py

# │   ├── test\_guardrails.py

# │   └── test\_path\_guard.py

# │

# ├── docs/

# ├── README.md

# └── .gitignore

# ```

#

# \## 5. Setup and Installation

#

# \### Prerequisites

#

# \- Python 3.10 or later.

# \- Ollama installed locally.

# \- Qwen2.5 7B model.

# \- Git.

# \- FUSE-compatible environment for filesystem mounting.

#

# \### Step 1: Clone the repository

#

# ```bash

# git clone https://github.com/iamlovelesh24/phantomnet-llm-honeypot.git

# cd phantomnet-llm-honeypot

# ```

#

# \### Step 2: Create a virtual environment

#

# ```bash

# python -m venv venv

# ```

#

# Activate it on Windows:

#

# ```powershell

# .\\venv\\Scripts\\Activate.ps1

# ```

#

# \### Step 3: Install dependencies

#

# Install the required Python packages and FUSE binding for your operating system.

#

# The project uses the Ollama Python client and pytest for LLM integration and testing.

#

# \### Step 4: Download the LLM

#

# ```bash

# ollama pull qwen2.5:7b

# ```

#

# Ensure the Ollama service is running locally before executing LLM evaluations.

#

# \## 6. Running the Project

#

# \### LLM Generation

#

# The LLM interface is implemented in:

#

# ```text

# llm/model.py

# ```

#

# The generation pipeline:

#

# 1\. Receives a user prompt.

# 2\. Validates the input using safety guardrails.

# 3\. Builds structured context when provided.

# 4\. Sends the messages to the local Ollama model.

# 5\. Validates the generated response.

# 6\. Returns the response or a safety message.

#

# \### Prompt Consistency Evaluation

#

# Run:

#

# ```bash

# python -m evaluation.prompt\_consistency

# ```

#

# This evaluates whether generated content remains consistent with the fictional NexusCore environment.

#

# \### Running the Test Suite

#

# Run all tests:

#

# ```bash

# python -m pytest tests/ -v

# ```

#

# Run individual test modules:

#

# ```bash

# python -m pytest tests/test\_guardrails.py -v

# python -m pytest tests/test\_path\_guard.py -v

# python -m pytest tests/test\_fuse\_fs.py -v

# python -m pytest tests/test\_file\_generator\_validation.py -v

# ```

#

# \## 7. Safety and Security

#

# PhantomNet includes safety mechanisms designed to maintain a controlled synthetic environment.

#

# \### LLM Guardrails

#

# \- Rejects prohibited real-world data requests.

# \- Validates generated output.

# \- Rejects empty or invalid input and output.

# \- Provides a standard safety response when validation fails.

#

# \### Filesystem Protection

#

# \- Restricts filesystem access to the configured sandbox.

# \- Blocks parent-directory traversal.

# \- Rejects invalid and relative paths.

# \- Protects against access outside the sandbox.

# \- Maintains read-only deception filesystem behavior.

#

# \## 8. Evaluation

#

# The project includes evaluation and testing for:

#

# \- Prompt consistency with fictional company lore.

# \- Employee and project identity consistency.

# \- Input and output safety validation.

# \- Filesystem path traversal protection.

# \- Synthetic file generation validation.

# \- FUSE filesystem behavior.

# \- Filesystem performance benchmarking.

#

# \## 9. Project Status

#

# The project has completed major implementation and validation work, including:

#

# \- Local LLM integration.

# \- Context-aware prompt generation.

# \- Fictional corporate environment.

# \- Safety guardrails and tests.

# \- Generative filesystem integration.

# \- Sandbox path validation.

# \- Prompt consistency evaluation.

#

# Final integration and documentation activities are part of the remaining project workflow.

#

# \## 10. Contributors

#

# Developed collaboratively as part of the \*\*Infotact Solutions Generative AI Internship\*\*.

#

# \- Member 1: LLM Integration and Evaluation.

# \- Member 2: Generative FUSE Filesystem and Deception Shell.

#

# \## 11. Disclaimer

#

# PhantomNet is an experimental cyber-deception project intended for controlled research, learning, and testing.

#

# It uses fictional organizational data and synthetic content. It is not intended to access, expose, or interact with real credentials, private records, or production systems.
