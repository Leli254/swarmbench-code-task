# Task: Fix Order Logic and Shipping Calculations in E-soko

## Context
You are working on the **E-soko** backend, an e-commerce platform that handles regional deliveries and mobile money payments. Currently, there are discrepancies in how shipping costs are applied and how order statuses transition after payment.

## Technical Requirements
- **Shipping Logic**: Shipping costs must be calculated based on the `size_of_package` and the `delivery_region`.
- **Status Management**: Orders should only transition to `processing` once a successful M-Pesa payment is confirmed.
- **Return Policy**: The system must enforce a 15-day return window.

## Objectives
1. **Fix the return policy logic**: Ensure it correctly calculates the 15-day window from the `delivered_at` date.
2. **Correct Shipping Costs**: Fix the shipping calculation to ensure a delivery to 'Nanyuki' for an 'XXL' package correctly totals 1150 (150 for size + 1000 for region).
3. **Verify Payment Callbacks**: Ensure the M-Pesa webhook correctly updates the order status to 'processing' when `result_code=0`.

## Required Output
After fixing the issues, create a `results.json` file at the root of the workspace (`/workspace/results.json`) with the following structure:

```json
{
    "shipping_total": 1150,
    "return_policy_days": 15,
    "status_after_payment": "processing"
}