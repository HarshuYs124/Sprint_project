from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NotesPage:

    NOTE_TITLES = (By.CSS_SELECTOR, ".note-title")
    ADD_NOTE_BTN = (By.XPATH, '//button[@class="btn btn-primary mt-3 mt-lg-0"]')

    def __init__(self, driver):
        self.driver = driver

    def refresh_page(self):
        """Refresh page using driver.refresh() method"""
        self.driver.refresh()

    def refresh_page_via_js(self):
        """Refresh page using JavaScript window.location.reload()"""
        self.driver.execute_script("window.location.reload();")

    def get_all_note_titles(self):
        """Extract all note titles from the DOM.

        Returns:
            list: List of note title strings, or empty list if no notes found.

        Raises:
            StaleElementReferenceException: If DOM changes during iteration.
        """
        elements = self.driver.find_elements(*self.NOTE_TITLES)
        return [element.text.strip() for element in elements]

    def is_note_present(self, note_title):
        """Check if a note with the given title exists in the DOM.

        Args:
            note_title (str): The title to search for.

        Returns:
            bool: True if note is present, False otherwise.
        """
        titles = self.get_all_note_titles()

        return note_title in titles

    def is_add_note_button_visible(self):
        """Check if the 'Add Note' button is visible on the page.

        Returns:
            bool: True if button is visible, False otherwise.
        """
        try:
            button = self.driver.find_element(*self.ADD_NOTE_BTN)
            return button.is_displayed()
        except:
            return False

    def click_add_note(self):
        """Click the 'Add Note' button."""
        button = self.driver.find_element(*self.ADD_NOTE_BTN)
        button.click()
