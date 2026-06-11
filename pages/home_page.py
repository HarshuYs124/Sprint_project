from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    add_note_btn = (By.XPATH, '//button[@class="btn btn-primary mt-3 mt-lg-0"]')

    notes_heading = (By.XPATH, "//h1[contains(text(),'My Notes')]")

    profile_btn = (By.XPATH, "//button[contains(@class,'dropdown-toggle')]")

    logout_btn = (By.XPATH, "//button[contains(text(),'Logout')]")
    view_btn = (By.XPATH, "//button[contains(text(),'View')]")
    edit_btn = (By.XPATH, "//button[contains(text(),'Edit')]")
    delete_btn = (By.XPATH, "//button[contains(text(),'Delete')]")
    ui_note_title_element = (By.XPATH, "//div[@data-testid='note-card-title']")
    ui_note_desc_element = (By.XPATH, "//div[contains(@class,'card')]//p")

    def click_add_note(self):
        self.click(self.add_note_btn)

    def click_profile(self):
        self.click(self.profile_btn)

    def logout(self):
        self.click_profile()
        self.click(self.logout_btn)

    def click_view(self):
        self.click(self.view_btn)

    def click_edit(self):
        self.click(self.edit_btn)

    def click_delete(self):
        self.click(self.delete_btn) 

    # Validation
    def is_home_page_displayed(self):
        return self.driver.find_element(*self.notes_heading).is_displayed()

    def is_note_present_on_ui(self, title, description):
        # Formulates an exact text-pair match strategy via localized XPath maps
        xpath_query = f"//div[contains(@class,'card')]//h5[text()='{title}']/following-sibling::p[text()='{description}']"
        try:
            return self.driver.find_element(By.XPATH, xpath_query).is_displayed()
        except Exception:
            return False

    def get_note_title(self):
        """Fetches the title string of the note from the web UI."""
        return self.driver.find_element(*self.ui_note_title_element).text

    def get_note_description(self):
        """Fetches the description string of the note from the web UI."""
        return self.driver.find_element(*self.ui_note_desc_element).text