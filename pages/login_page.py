from pages.base_page import BasePage
from playwright.sync_api import expect, TimeoutError

class LoginPage(BasePage):

    #  SELECTORS (MUI SAFE) 
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    LOGIN_BTN = "button.MuiButton-contained:has-text('Login')"
    ERROR_MSG = "text=Invalid"
    CLOSE_MODAL_BTN = "button[aria-label='close']"  # X button selector
    INCORRECT_CRED = "div.MuiAlert-message:has-text('Incorrect email or password')"
    EMAIL_REQUIRED = "p#email-helper-text"
    PASSWORD_REQUIRED = "p#password-helper-text"

    def close_modal_if_present(self):
        modal_close = self.page.locator(self.CLOSE_MODAL_BTN)
        if modal_close.count() > 0 and modal_close.is_visible():
            modal_close.click(force=True)

    #  ACTIONS
    def login(self, email, password):
        # Close modal if exists
        self.close_modal_if_present()

        email_input = self.page.locator(self.EMAIL)
        password_input = self.page.locator(self.PASSWORD)
        login_btn = self.page.locator(self.LOGIN_BTN).first  # pick first match

        # Fill email + trigger validation
        email_input.fill(email)
        email_input.press("Tab")

        # Fill password + trigger validation
        password_input.fill(password)
        password_input.press("Tab")

        # Wait for login button visible & enabled
        login_btn.wait_for(state="visible", timeout=5000)
        expect(login_btn).to_be_enabled(timeout=5000)

        # Force click login button
        login_btn.click(force=True)

    #  ASSERTIONS 
    def error_displayed(self):
        return self.get_error_message() is not None

    def get_error_message(self, timeout=5000):
        """
        Returns the visible error message text or None if not found.
        Also logs the message for CI/CD.
        """

        locators = [
            self.INCORRECT_CRED,
            self.EMAIL_REQUIRED,
            self.PASSWORD_REQUIRED,
        
        ]

        for locator in locators:
            try:
                el = self.page.locator(locator)
                el.wait_for(state="visible", timeout=timeout)

                text = el.inner_text().strip()
                print(f"[LOG] Error shown: {text}")  # CI/CD logging

                # SAFE screenshot filename 
                safe_text = "".join(c for c in text if c.isalnum())[:15]
                self.page.screenshot(
                    path=f"screenshots/login_error_{safe_text}.png"
                )

                return text

            except TimeoutError:
                continue

        return None
