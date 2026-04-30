#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Initializing E-soko Test Suite ---"

# 1. Setup Environment
# Ensure we are in the workspace
cd /workspace

# 2. Run the Validation Tests
# We use pytest to run our logic checks. The results are saved in an XML file for further analysis.
echo "Running Django Logic Tests..."
pytest tests/test_logic.py --junitxml=results.xml

# 3. Check for specific success criteria in the output
# For example, verifying the Nanyuki shipping math we defined in dataset.csv
if grep -q "test_shipping_calculation_nanyuki_xxl PASSED" results.xml; then
    echo "SUCCESS: Shipping logic verified."
else
    echo "FAILURE: Shipping logic mismatch."
    exit 1
fi

# 4. Final Verification
echo "--- All SwarmBench Tests Passed ---"
exit 0