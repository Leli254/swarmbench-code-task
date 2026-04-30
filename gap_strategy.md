# Gap Strategy: E-soko Logic Validation

## 1. The 40-Point Gap Definition
A standard LLM typically fails this task because it treats the files in isolation. While it might fix a math error in `models.py`, it often misses how that change affects the `MpesaPayment` validation or the final `test.sh` assertions. 

## 2. Complexity Dimensions
- **Cross-Module Dependency**: The shipping cost is defined in `Shop`, but used in `Orders`, and verified against the `Stripe` checkout session. An agent must trace this flow across three files[cite: 1, 3].
- **Temporal Logic**: The `check_returnable` method requires understanding `timezone.now()` vs `delivered_at`. Standard models often struggle with date arithmetic and "15-day" boundary conditions in a mock environment.
- **Asynchronous State**: The M-Pesa integration relies on a callback (`ResultCode`). The agent must simulate the webhook response to see if the `Order` state actually flips to `paid`[cite: 2, 3].

## 3. Swarm Advantage
- **The "Auditor" Role**: By separating the "Auditor" from the "Coder," we ensure the logic is mapped before a single line of code is changed.
- **Verification Loop**: The "QA Engineer" agent will execute `test.sh` multiple times, forcing the "Developer" agent to iterate until the shipping math (e.g., $150 + 1000 = 1150$) is perfect[cite: 1].
- **Specialization**: A specialized "Fintech" agent will recognize M-Pesa `CheckoutRequestID` patterns that a general model might ignore[cite: 2].