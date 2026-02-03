from playwright.sync_api import Page, expect
import re

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Locators        
        self.thankyou_message = page.get_by_text("Thank you for being a part of the global TCF family!")
        self.welcome_message = page.get_by_text(re.compile("Welcome", re.IGNORECASE))


        self.profile_icon = page.locator(".user-profile-icon") # Example selector
        self.logout_button = page.get_by_role("button", name="Logout")

    
    def verify_dashboard_opened(self):
        """
        Ye method wait_for_selector ka kaam karega lekin modern tarike se.
        """
        #10 sec smart wait
        expect(self.welcome_message).to_be_visible(timeout=10000)
        expect(self.thankyou_message).to_be_visible(timeout=10000)
        return True 
    
    def is_loaded(self):
        # Safety check boolean return
        try:
            expect(self.thankyou_message).to_be_visible(timeout=5000)
            return True
        except AssertionError:
            return False