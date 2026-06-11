from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):


    add_note_btn = (By.XPATH, '//button[@class="btn btn-primary mt-3 mt-lg-0"]')
    category_dropdown = (By.ID, "category")
    completed_checkbox = (By.ID, "completed")
    title_input = (By.ID, "title")
    description_input = (By.ID, "description")
    create_btn = (By.XPATH, "//button[contains(text(),'Create')]")
    cancel_btn = (By.XPATH, "//button[contains(text(),'Cancel')]")
    description_error = (By.XPATH, "//div[contains(text(),'Description is required')]")
    created_note_title = (By.XPATH, "//div[@data-testid='note-card-title']")
    created_note_description = (By.XPATH, "//p[@class='card-text']")

    def click_add_note(self):
        self.click(self.add_note_btn)

    def select_category(self, category):
        self.select_option(self.category_dropdown, category)

    def mark_completed(self):
        self.click(self.completed_checkbox)

    def enter_title(self, title):
        self.enter_text(self.title_input, title)

    def enter_description(self, description):
        self.enter_text(self.description_input, description)

    def click_create(self):
        self.click(self.create_btn)

    def create_note(self, category, title, description, completed=False):

        self.click_add_note()

        self.select_category(category)

        if completed:
            self.mark_completed()

        self.enter_title(title)
        self.enter_description(description)

        self.click_create()

    def get_description_error_message(self):
        return self.get_text(self.description_error)

    def get_note_title(self):
        return self.get_element(self.created_note_title).text

    def get_note_description(self):
        return self.get_element(self.created_note_description).text

