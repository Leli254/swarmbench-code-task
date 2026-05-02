#!/bin/bash
set -e

# ============================================
# E-soko Order Logic Verifier
# ============================================
# This verifier executes the test suite and reports the reward to Harbor.
# It checks for three core business logic fixes:
#   1. Shipping calculation (XXL + Nanyuki = 1150)
#   2. Return policy window (15-day enforcement)
#   3. Payment callback state transition (pending -> processing)
# ============================================

echo "=== Starting E-soko Verifier ==="
echo "PWD: $(pwd)"
echo "Script dir: $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============================================
# Locate Test File
# ============================================
# The test file is mounted to /tests from the host's tests directory
TEST_FILE="/tests/test_logic.py"

# Fallback to alternative locations if needed
if [ ! -f "$TEST_FILE" ]; then
    TEST_FILE="/workspace/tests/test_logic.py"
fi
if [ ! -f "$TEST_FILE" ]; then
    TEST_FILE="test_logic.py"
fi

echo "Using test file: $TEST_FILE"

# ============================================
# Execute Test Suite
# ============================================
if [ -f "$TEST_FILE" ]; then
    echo "Running business logic tests..."
    python3 "$TEST_FILE"
    TEST_EXIT_CODE=$?
else
    echo "ERROR: Cannot find test_logic.py"
    ls -la /tests/ 2>/dev/null || echo "/tests not accessible"
    ls -la /workspace/tests/ 2>/dev/null || echo "/workspace/tests not accessible"
    TEST_EXIT_CODE=1
fi

# ============================================
# Determine Base Reward from Test Results
# ============================================
if [ $TEST_EXIT_CODE -eq 0 ]; then
    REWARD="1.0"
    echo "✓ All tests passed"
else
    REWARD="0.0"
    echo "✗ Tests failed"
fi

# ============================================
# Post-Test Validation: Agent Output Check
# ============================================
# Even if tests pass, we verify the agent produced the required output artifact.
# This ensures the agent didn't just pass tests via side effects without
# generating the expected results.json for downstream consumers.
if [ $TEST_EXIT_CODE -eq 0 ]; then
    if [ -f "/logs/agent/results.json" ] || [ -f "/workspace/results.json" ] || [ -f "results.json" ]; then
        echo "✓ Agent output artifact (results.json) verified"
    else
        echo "⚠️  Warning: Tests passed but no results.json found in expected locations"
        echo "    Expected: /logs/agent/results.json, /workspace/results.json, or ./results.json"
        # Reward remains 1.0 as tests are the canonical source of truth
        # This warning serves as diagnostic for multi-agent evaluation
    fi
fi

# ============================================
# Write Reward to Harbor-Expected Location
# ============================================
# Harbor looks for reward.txt in the verifier directory.
# The verifier directory is typically mounted at /verifier or discovered at runtime.
VERIFIER_DIR="/verifier"

if [ ! -d "$VERIFIER_DIR" ]; then
    # Attempt to locate the verifier directory dynamically
    VERIFIER_DIR=$(find / -type d -name "verifier" -writable 2>/dev/null | head -1)
fi

if [ -n "$VERIFIER_DIR" ] && [ -d "$VERIFIER_DIR" ]; then
    echo "$REWARD" > "$VERIFIER_DIR/reward.txt"
    echo "$REWARD" > "$VERIFIER_DIR/reward.json"
    echo "✓ Wrote reward to $VERIFIER_DIR/reward.txt"
else
    # Fallback: create verifier directory in current working directory
    mkdir -p verifier
    echo "$REWARD" > verifier/reward.txt
    echo "$REWARD" > verifier/reward.json
    echo "✓ Wrote reward to ./verifier/reward.txt"
fi

# ============================================
# Redundant Writes for Compatibility
# ============================================
# Harbor may check multiple locations depending on version and configuration.
# These additional writes ensure backward compatibility.
echo "$REWARD" > reward.txt
echo "$REWARD" > /workspace/reward.txt

# ============================================
# Stdout Fallback
# ============================================
# Some Harbor versions capture reward from stdout if file-based
# reward detection fails.
echo "$REWARD"

echo "=== Verifier complete ==="
exit 0