import pytest
from playwright.sync_api import sync_playwright
from utils.env_reader import env

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
                                  
            slow_mo=1000  )

        context = browser.new_context(
            http_credentials={
                "username": env("HTTP_USER"),
                "password": env("HTTP_PASS")
            }
        )

        page = context.new_page()
        page.goto(env("BASE_URL"))

        yield page
        browser.close()
