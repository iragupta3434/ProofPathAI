# ProofPath AI

**An agentic evidence assistant for refunds, warranties, damaged deliveries, and complaints.**

## Problem
People often struggle to organize evidence, identify missing information, and determine the next step when resolving refund, warranty, or service complaints.

## Solution
ProofPath AI helps users organize evidence, identify missing details, and prepare practical next steps based on information and policies provided by the user.

## Current Features
- Case-specific guidance for refunds, warranties, damaged deliveries, and service complaints
- Evidence checklist and missing-information prompts
- Local JSON-based case tracking
- Case status and next-action updates
- Agent Chat Protocol (ACP) integration with Agentverse

## Technology Stack
- Python
- Fetch.ai uAgents
- Agent Chat Protocol (ACP)
- Agentverse
- ASI:One API

## Run Locally
Install the dependencies:

```bash
python -m pip install requests uagents uagents-core python-dotenv
```

Run the Coordinator:

```bash
python agent.py
```

Run the case tracker demo:

```bash
python case_tracker.py
```

Test the ASI:One API:

```bash
python test_asi1.py
```

## Roadmap
- Integrate the Evidence Analyst agent
- Add policy analysis and resolution planning
- Connect case tracking to the Coordinator
- Test the complete workflow through ASI:One

## Disclaimer
ProofPath AI provides informational guidance, not legal advice. Recommendations depend on the evidence and policies supplied. It does not guarantee refunds or claim outcomes.
