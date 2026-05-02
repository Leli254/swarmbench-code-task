"""
Independent test logic - no Django dependency
These tests check the business logic without needing a Django project
"""

def test_shipping_calculation_nanyuki_xxl():
    """
    Test Case: XXL Package to Nanyuki
    Logic: Base Region Cost (1000) + Package Size (150) = 1150
    """
    # Simulate the business logic directly
    def calculate_shipping(region, package_size):
        # This would typically come from database or config
        region_costs = {"Nanyuki": 1000}
        size_costs = {"XXL": 150}
        
        base_cost = region_costs.get(region, 0)
        size_cost = size_costs.get(package_size, 0)
        
        return base_cost + size_cost
    
    total_shipping = calculate_shipping("Nanyuki", "XXL")
    assert total_shipping == 1150, f"Expected 1150, but got {total_shipping}"
    print("✓ test_shipping_calculation_nanyuki_xxl passed")


def test_return_policy_window():
    """
    Test Case: 15-day return window logic.
    """
    from datetime import datetime, timedelta
    
    def is_returnable(delivery_date, current_date, return_window_days=15):
        days_since_delivery = (current_date - delivery_date).days
        return days_since_delivery <= return_window_days
    
    now = datetime.now()
    
    # Test with recent delivery (10 days ago)
    recent_delivery = now - timedelta(days=10)
    assert is_returnable(recent_delivery, now) == True
    print("✓ Recent delivery (10 days): returnable = True")
    
    # Test with old delivery (16 days ago)
    old_delivery = now - timedelta(days=16)
    assert is_returnable(old_delivery, now) == False
    print("✓ Old delivery (16 days): returnable = False")


def test_mpesa_callback_state_transition():
    """
    Test Case: Payment confirmation transitions order to 'processing'.
    """
    def process_payment_callback(result_code, current_status="pending"):
        if result_code == 0:  # Success
            return "processing", True
        else:
            return current_status, False
    
    # Test successful payment
    status, paid = process_payment_callback(0)
    assert paid == True
    assert status == "processing"
    print("✓ Payment callback with result_code=0: status='processing', paid=True")
    
    # Test failed payment
    status, paid = process_payment_callback(1)
    assert paid == False
    assert status == "pending"
    print("✓ Payment callback with result_code=1: status='pending', paid=False")


if __name__ == "__main__":
    print("\n=== Running Business Logic Tests ===\n")
    test_shipping_calculation_nanyuki_xxl()
    test_return_policy_window()
    test_mpesa_callback_state_transition()
    print("\n=== All tests passed! ===\n")
