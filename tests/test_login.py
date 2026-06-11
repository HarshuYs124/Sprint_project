import pytest

from pages.login_page import LoginPage
from Config.environment import ConfigReader
from time import sleep
import datetime
import os

@pytest.mark.order(1)
def test_invalid_login(setup_and_teardown):
    driver = setup_and_teardown

    config = ConfigReader.read_config()
    env = config["qa"]

    email = env["invalid_email"]
    password = env["invalid_password"]

    lp = LoginPage(driver)

    lp.click_login_link()
    lp.enter_email(email)
    lp.enter_password(password)
    lp.click_login_button()
    sleep(3)
    os.makedirs("screenshots", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/invalid_login_{timestamp}.png"

    driver.save_screenshot(screenshot_path)

    print(f"Screenshot saved at: {screenshot_path}")
    sleep(3)

    assert driver.current_url != "https://practice.expandtesting.com/notes/app"


@pytest.mark.order(2)
def test_valid_login(setup_and_teardown):
    driver = setup_and_teardown

    config = ConfigReader.read_config()
    env = config["qa"]
    email = env["email"]
    password = env["password"]

    lp = LoginPage(driver)
    lp.enter_email(email)
    lp.enter_password(password)
    lp.click_login_button()

    sleep(3)

