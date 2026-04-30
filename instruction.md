# Task: Fix Order Logic and Shipping Calculations in E-soko

## Context
You are working on the **E-soko** backend, an e-commerce platform that handles regional deliveries and mobile money payments. Currently, there are discrepancies in how shipping costs are applied and how order statuses transition after payment.

## Technical Requirements
- **Shipping Logic**: Shipping costs must be calculated based on the `size_of_package` and the `delivery_region`.
- **Status Management**: Orders should only transition to `processing` once a successful M-Pesa or Stripe payment is confirmed.
- **Return Policy**: The system must enforce a 15-day return window.

## Objectives
1. **Debug the `check_returnable` method**: Ensure it correctly calculates the 15-day window from the `delivered_at` date.
2. **Correct Shipping Costs**: Fix the `get_shipping_cost` logic to ensure a delivery to 'Nanyuki' for an 'XXL' package correctly totals 1150 (150 for size + 1000 for region).
3. **Verify Payment Callbacks**: Ensure that the M-Pesa webhook correctly updates the `paid` status of the associated `Order` object.

## Constraints
- Do not modify the database schema.
- All fixes must pass the existing test suite in `/workspace/tests/`.
- Ensure all image processing remains optimized at $300 \times 300$ resolution.