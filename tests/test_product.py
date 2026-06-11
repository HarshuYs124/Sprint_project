import pytest

from pages.product_page import ProductPage
from Config.environment import ConfigReader
from time import sleep
import datetime

@pytest.mark.order(3)
def test_invalid_product(setup_and_teardown):
    driver = setup_and_teardown

    config = ConfigReader.read_config()
    env = config["qa"]

    category = env["category"]
    title = env["title"]


    pp = ProductPage(driver)

    pp.click_add_note()
    pp.select_category(category)
    pp.enter_title(title)
    pp.click_create()
    sleep(3)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/invalid_Note_{timestamp}.png"

    driver.save_screenshot(screenshot_path)

    print(f"Screenshot saved at: {screenshot_path}")
    sleep(3)

    error_message = pp.get_description_error_message()

    assert error_message == "Description is required"

@pytest.mark.order(4)
def test_valid_product(setup_and_teardown):
    driver = setup_and_teardown

    config = ConfigReader.read_config()
    env = config["qa"]

    category = env["category"]
    title = env["title"]
    description = env["description"]


    pp = ProductPage(driver)
    pp.select_category(category)

    pp.enter_title(title)
    pp.enter_description(description)
    pp.click_create()
    sleep(3)

    actual_title = pp.get_note_title()
    actual_description = pp.get_note_description()

    print(actual_title)
    print(actual_description)

    assert actual_title == title
    assert actual_description == description

