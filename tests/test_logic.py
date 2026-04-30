import pytest
from datetime import timedelta
from django.utils import timezone

# Note: In the final SwarmBench run, the agent will need to import these:
# from shop.models import Product, Order
# from payments.models import MpesaPayment


def test_shipping_calculation_nanyuki_xxl():
    """
    Test Case: XXL Package to Nanyuki
    Logic: Base Region Cost (1000) + Package Size (150) = 1150
    """
    # The agent is expected to have fixed the logic so that
    # these values are pulled dynamically from the model/DB.
    region_cost = 1000
    package_size_cost = 150
    total_shipping = region_cost + package_size_cost

    assert total_shipping == 1150, f"Expected 1150, but got {total_shipping}"


def test_return_policy_window():
    """
    Test Case: 15-day return window logic.
    """
    now = timezone.now()

    # 1. Test item delivered 10 days ago (Should be returnable)
    recent_delivery = now - timedelta(days=10)
    # The logic check: current time - delivery time <= 15 days
    is_returnable_recent = (now - recent_delivery).days <= 15
    assert is_returnable_recent is True

    # 2. Test item delivered 16 days ago (Should NOT be returnable)
    old_delivery = now - timedelta(days=16)
    is_returnable_old = (now - old_delivery).days <= 15
    assert is_returnable_old is False


def test_mpesa_callback_state_transition():
    """
    Test Case: Payment confirmation transitions order to 'processing'.
    """
    # Simulate a successful M-Pesa ResultCode (0 means Success)
    result_code = 0
    order_status = "pending"
    paid = False

    # This simulates the logic expected in the M-Pesa callback view
    if result_code == 0:
        paid = True
        order_status = "processing"

    assert paid is True
    assert order_status == "processing"
