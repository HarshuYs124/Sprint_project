from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


class BasePage:


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self,locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self,locator,text):
        self.wait.until(EC.element_to_be_clickable(locator)).clear()
        self.wait.until(EC.element_to_be_clickable(locator)).send_keys(text)

    def get_element(self,locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def scroll_to_element(self, locator):
        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

    def select_option(self,locator,text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        Select(element).select_by_visible_text(text)

    def get_text(self, locator):
        return self.driver.find_element(*locator).text

    def get_texts(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text