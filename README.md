🚀 SwarmBench — Multi-Agent Orchestration & Benchmark Framework

SwarmBench is a structured framework for designing, executing, and evaluating multi-agent AI systems on complex, decomposable tasks.

It focuses on a core hypothesis:

Certain classes of problems are structurally better solved by coordinated agent swarms rather than a single agent.

This repository implements a full pipeline for:

Task design
Agent decomposition
Parallel execution
Result synthesis
Deterministic verification
🧠 Core Concept

Traditional single-agent systems struggle with:

Large context windows
Multi-step coordination
Coverage across many artifacts
Consistency during synthesis

SwarmBench addresses this by enabling:

Task → Decomposition → Parallel Agents → Reducer → Verified Output

Where:

Independent subproblems are solved in parallel
Outputs are reconciled into a final result
A verifier enforces correctness and completeness
⚙️ System Architecture
.
├── instruction.md        # Task definition (agent-facing, role-neutral)
├── task.toml             # Metadata, constraints, execution config
├── decomposition.yaml    # Multi-agent orchestration plan
├── environment/
│   └── Dockerfile        # Runtime environment
├── tests/
│   ├── test.sh           # Entry point for verification
│   ├── verify.py         # Deterministic scoring logic
│   └── judge.py          # (Optional) LLM-based evaluation
├── solution/
│   └── solve.sh          # Oracle solution (ground truth)
🔁 Execution Flow

SwarmBench runs through a controlled pipeline:

Build container from environment/Dockerfile
Load task from instruction.md
Execute agent(s) inside container
Run verification via tests/test.sh
Compute reward score (0.0 → 1.0)
Store logs and outputs
🧩 Multi-Agent Coordination

SwarmBench supports structured decomposition strategies:

Fan-out / Synthesize
Independent agents solve isolated subproblems
A reducer merges and validates outputs
Map / Reduce
Work is distributed across shards
Aggregation ensures global consistency

Defined in:

decomposition.yaml

Each sub-task specifies:

Scope of responsibility
Input artifacts
Expected output
Dependencies
🧪 Verification Model

SwarmBench enforces objective scoring:

Executable Verifier
Deterministic checks (files, outputs, structure)
Weighted scoring system
Produces reward.txt
LLM Judge (Optional)
Evaluates open-ended outputs
Uses rubric + evidence validation
Assigns partial credit
🧬 Oracle System

The oracle defines the ground truth solution path.

solution/solve.sh

It must:

Produce the expected output
Pass all verification checks
Score 1.0

This guarantees:

Task validity
Verifier correctness
End-to-end consistency
🐳 Environment Isolation

Each task runs in a containerized environment:

Reproducible execution
Controlled dependencies
No hidden state

Defined in:

environment/Dockerfile
🚀 Running the System
1. Setup
git clone <your-repo>
cd harbor

Ensure Docker is running.

2. Run Oracle
uv run harbor run \
  -p /path/to/task \
  -a oracle \
  -k 1 \
  -n 1 \
  --job-name "oracle" \
  --jobs-dir /path/to/logs

Expected:

reward = 1.0
🎯 Design Principles

SwarmBench is built around tasks that naturally require:

Decomposition
Parallel execution
Aggregation
Consistency validation

Strong task patterns include:

Multi-file code fixes
Multi-source data extraction
Cross-dataset reconciliation
Constraint-heavy planning
⚠️ Anti-Patterns

Tasks that do not benefit from multi-agent systems:

Single bug fixes
Linear workflows
One-step computations
Small isolated problems
📊 Scoring Philosophy

A well-designed task produces:

System Type	Expected Score
Oracle	1.0
Multi-Agent	~1.0
Single-Agent	≤ 0.6

This creates a measurable performance gap driven by structure, not trickery.

🧱 Extending SwarmBench

You can build new tasks by:

Defining a complex, decomposable problem
Creating clear sub-task boundaries
Implementing a verifier with partial scoring
Providing an oracle solution
Validating end-to-end execution
🛠 Tech Stack
Python 3.11+
Docker
Shell scripting
Structured YAML / TOML configs
Optional LLM-based evaluation
📌 Use Cases
Benchmarking multi-agent systems
Evaluating orchestration strategies
Stress-testing LLM coordination limits
Research on distributed AI problem solving
🧭 Philosophy

SwarmBench is not about making tasks harder.

It’s about making them structurally realistic—
the kind of problems that naturally demand coordination, not just intelligence.

📄 License

MIT License (or your preferred license)

👤 Author

Michael Leli
