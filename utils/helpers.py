from playwright.sync_api import TimeoutError
import logging
import os
from datetime import datetime
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_logs.log"),
        logging.StreamHandler()
    ]
)

def wait_for_url_contains(page, text, timeout=5000):
    """Wait until the current URL contains `text`. Returns True if found, else False."""
    try:
        page.wait_for_url(f"**{text}**", timeout=timeout)
        logging.info(f"URL contains expected text: '{text}'")
        return True
    except TimeoutError:
        logging.error(f"URL did not contain expected text within {timeout}ms: '{text}'")
        return False

def is_error_visible(page, locator):
    """Check if the error message or any element is visible."""
    try:
        visible = page.locator(locator).is_visible()
        logging.info(f"Error visibility for locator '{locator}': {visible}")
        return visible
    except Exception as e:
        logging.error(f"Error checking visibility for locator '{locator}': {e}")
        return False



def take_screenshot(page, name=None):
    """Take a screenshot with timestamp and optional name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not name:
        filename = f"screenshot_{timestamp}.png"
    else:
        # sanitize name for filesystem
        safe_name = re.sub(r"[^\w\d_-]", "_", name)
        filename = f"{safe_name}_{timestamp}.png"

    filepath = os.path.join("screenshots", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    page.screenshot(path=filepath, full_page=True)
    logging.info(f"Screenshot saved: {filepath}")
    return filepath

