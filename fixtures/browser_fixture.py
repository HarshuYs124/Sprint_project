import pytest
from selenium.webdriver import Chrome,ChromeOptions
from Config.environment import ConfigReader
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def setup_and_teardown():
    # Reading the config
    config = ConfigReader.read_config()
    env = config["qa"]
    base_url = env["base_url"]
    # Setup
    o = ChromeOptions()
    o.add_experimental_option("detach", True)
    driver = Chrome(options=o)
    driver.maximize_window()
    driver.get(base_url)

    yield driver

    # Teardown
    driver.quit()



@pytest.fixture(scope="function")
def login_fixture():
    """Fixture that provides a logged-in driver for each test (function scope).
    Enables parallel execution with pytest-xdist."""
    # Reading the config
    config = ConfigReader.read_config()
    env = config["qa"]
    base_url = env["base_url"]
    email = env["email"]
    password = env["password"]

    # Setup
    o = ChromeOptions()
    o.add_experimental_option("detach", True)
    driver = Chrome(options=o)
    driver.maximize_window()
    driver.get(base_url)

    # Perform login
    login_page = LoginPage(driver)
    login_page.click_login_link()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_login_button()


    yield driver

    # Teardown
    driver.quit()
