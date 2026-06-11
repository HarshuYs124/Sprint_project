from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from time import sleep

class LoginPage(BasePage):

    login_button = (By.XPATH, "//a[@href='/notes/app/login']")
    email_input = (By.ID, "email")
    password_input = (By.ID, "password")
    lg_button = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        super().__init__(driver)


    def click_login_link(self):
        self.scroll_to_element(self.login_button)
        self.click(self.login_button)


    def enter_email(self, email):
        self.enter_text(self.email_input, email)

    def enter_password(self, password):
        self.enter_text(self.password_input, password)

    def click_login_button(self):
        self.scroll_to_element(self.lg_button)
        sleep(1)
        self.click(self.lg_button)

    def login(self, email, password):
        self.click_login_link()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()