import pytest
import logging
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.env_reader import env

logger = logging.getLogger(__name__)

# -------------------------
# POSITIVE LOGIN (SMOKE)
# -------------------------

@pytest.mark.smoke
@pytest.mark.login
def test_valid_login(page):
    """
    Test Case: Valid Login
    Description:
        Verify that a user can successfully log in with valid credentials.
        After login, user should land on dashboard page.
    """
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    logger.info("Starting valid login test")

    login.login(env("VALID_EMAIL"), env("VALID_PASSWORD"))

    assert dashboard.verify_dashboard_opened(), \
        "Dashboard not visible after valid login"

    assert "/profile" in page.url, \
        f"Unexpected URL after login: {page.url}"

    logger.info("Valid login successful, dashboard verified")

# -------------------------
# NEGATIVE LOGIN (REGRESSION)
# -------------------------

@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize(
    "email,password,expected_error",
    [
        (env("INVALID_EMAIL"), env("VALID_PASSWORD"), "Incorrect email or password"),
        (env("VALID_EMAIL"), env("INVALID_PASSWORD"), "Incorrect email or password"),
        (env("INVALID_EMAIL"), env("INVALID_PASSWORD"), "Incorrect email or password"),
        ("", env("VALID_PASSWORD"), "Email is required"),
        (env("VALID_EMAIL"), "", "Password is required"),
        ("", "", "Email is required"),
    ],
    ids=[
        "Invalid Email",
        "Invalid Password",
        "Both Invalid",
        "Empty Email",
        "Empty Password",
        "Both Empty",
    ],
)
def test_invalid_login_cases(page, email, password, expected_error):
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    logger.info(f"Testing invalid login | Email='{email}' Password='{password}'")

    login.login(email, password)

    # User should stay on login page
    assert "login" in page.url, \
        "User redirected away from login page on invalid login"

    # Error message validation
    error_text = login.get_error_message()
    logger.info(f"Negative login error shown: '{error_text}'")

    assert error_text is not None, \
        "Expected error message not displayed"

    assert expected_error in error_text, \
        f"Expected '{expected_error}', got '{error_text}'"

    # Dashboard must NOT load
    assert not dashboard.is_loaded(), \
        "Dashboard loaded even though login should have failed"
