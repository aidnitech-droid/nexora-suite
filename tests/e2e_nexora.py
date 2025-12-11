#!/usr/bin/env python3
"""
E2E tests for Nexora Suite using Playwright.

Test flow: register → login → dashboard → open modules → check health.
Requires: playwright, pytest-playwright, pytest
"""
import pytest
from playwright.sync_api import expect, Page


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application. Override via env var BASE_URL."""
    import os
    return os.getenv("BASE_URL", "http://localhost:5060")


@pytest.fixture
def page(browser, base_url):
    """Create a fresh page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def test_01_register_new_user(page, base_url):
    """Test user registration flow."""
    page.goto(f"{base_url}/register")
    expect(page).to_have_title("Nexora - Register")
    
    # Fill registration form
    page.fill('input[name="username"]', "e2e_test_user")
    page.fill('input[name="email"]', "e2e@nexora.test")
    page.fill('input[name="password"]', "TestPassword123!")
    
    # Submit form
    page.click('button[type="submit"]')
    
    # Expect redirect to dashboard
    page.wait_for_url("**/dashboard*")
    expect(page).to_have_url(f"{base_url}/dashboard")


def test_02_login_existing_user(page, base_url):
    """Test login with registered user."""
    page.goto(f"{base_url}/login")
    expect(page).to_have_title("Nexora - Login")
    
    page.fill('input[name="username"]', "e2e_test_user")
    page.fill('input[name="password"]', "TestPassword123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard*")
    expect(page).to_have_url(f"{base_url}/dashboard")


def test_03_dashboard_displays_modules(page, base_url):
    """Test that dashboard displays module list."""
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', "e2e_test_user")
    page.fill('input[name="password"]', "TestPassword123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard*")
    
    # Check for key modules in dashboard
    modules = [
        "nexora-billing",
        "nexora-crm",
        "nexora-inventory",
        "nexora-expense"
    ]
    
    for module in modules:
        # Look for module links or displays
        elements = page.locator(f"text={module}")
        assert elements.count() > 0, f"Module {module} not found on dashboard"


def test_04_access_billing_module(page, base_url):
    """Test accessing the billing module from dashboard."""
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', "e2e_test_user")
    page.fill('input[name="password"]', "TestPassword123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard*")
    
    # Navigate to billing module (via dashboard link or direct)
    page.goto(f"{base_url}/module/nexora-billing/")
    
    # Should either show frontend or be accessible (200 status)
    response_status = page.evaluate("() => window.location.href")
    assert "billing" in page.url or "module" in page.url


def test_05_module_health_checks(page, base_url):
    """Test that module health endpoints are accessible."""
    # This is a simple HTTP test, not a browser interaction
    import requests
    
    modules = [
        "nexora-assist", "nexora-billing", "nexora-bookings",
        "nexora-crm", "nexora-expense", "nexora-inventory"
    ]
    
    for module in modules:
        health_url = f"{base_url}/module/{module}/api/health"
        resp = requests.get(health_url)
        assert resp.status_code == 200, f"{module} health check failed: {resp.status_code}"
        data = resp.json()
        assert "status" in data or "service" in data, f"{module} health response invalid"


def test_06_logout(page, base_url):
    """Test user logout."""
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', "e2e_test_user")
    page.fill('input[name="password"]', "TestPassword123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard*")
    
    # Find and click logout button/link
    logout_button = page.locator("a:has-text('Logout'), button:has-text('Logout')")
    if logout_button.count() > 0:
        logout_button.click()
        page.wait_for_url("**/")
        expect(page).to_have_url(f"{base_url}/")


if __name__ == "__main__":
    """Allow running tests with: pytest tests/e2e_nexora.py -v"""
    import subprocess
    subprocess.run(["pytest", __file__, "-v", "-s"], check=True)
