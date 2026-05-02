# Gap Strategy: E-soko Logic Validation

## 1. The 40-Point Gap Definition
A standard Large Language Model (LLM) typically fails this task because it attempts to resolve bugs in isolation. While a model might successfully fix a math error in `models.py`, it often fails to account for how that change must propagate through the M-Pesa payment validation hooks and the final `test.sh` assertion suite. The "gap" represents the delta between local code fixes and global system consistency.

## 2. Complexity Dimensions
*   **Cross-Module Dependency**: Shipping cost logic is defined within the `Shop` domain but consumed by `Orders` and verified against regional overrides in the payment layer. An agent must successfully trace state and data flow across three distinct modules to pass.
*   **Temporal Logic**: The `check_returnable` method requires precise date arithmetic using `timezone.now()` against the `delivered_at` timestamp. General-purpose models frequently struggle with 15-day boundary conditions and timezone-aware object comparisons in a mock environment.
*   **Asynchronous State Machine**: The integration relies on an M-Pesa callback mechanism (`ResultCode`). The agent must accurately simulate the asynchronous webhook response to verify that the `Order` state transitions correctly from `paid` to `processing`.

## 3. Swarm Advantage
*   **The Auditor/Coder Separation**: By utilizing a dedicated "Auditor" sub-task, the system logic is mapped and the Method Resolution Order (MRO) is understood before any code is modified, preventing hallucinated or conflicting fixes.
*   **Iterative Verification Loop**: A "Synthesizer" role acts as a QA lead, executing the `test.sh` suite multiple times. This forces the "Developer" agents to iterate until the composite shipping math (150 base + 1000 regional surcharge = 1150) is exact.
*   **Domain Specialization**: Specialized sub-agents focus on Fintech (M-Pesa callback patterns) and E-commerce (shipping/return arithmetic) independently, preventing the context-window saturation that often leads to regressions in single-agent attempts.

## 4. Expected Score Pattern
| Configuration | Expected Score | Reason |
| :--- | :--- | :--- |
| **Oracle** | 1.0 | Verified ground-truth solution with all logic paths cleared. |
| **Single-agent** | 0.3 - 0.6 | Typically resolves the math error but fails the temporal or state logic. |
| **Multi-agent** | 0.9 - 1.0 | Parallel sub-agents handle module-specific bugs without cross-contamination. |
| **Target Gap** | 40+ points | Represents the failure of monolithic agents to handle structural complexity. |

## 5. Oracle Validation
*   **Oracle Run Completed**: Yes (2026-05-01)
*   **Oracle Reward**: 1.0
*   **Command Used**: `harbor run -a oracle -k 1 -n 1`
*   **Notes**: Validation confirmed that the shipping total for XXL/Nanyuki orders yields exactly 1150 and the 15-day return window is strictly enforced.