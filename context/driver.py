import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from context.config import settings


class Driver(object):
    """Singleton class for interacting with the selenium webdriver object"""
    instance = None

    class SeleniumDriverNotFound(Exception):
        pass

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = Driver()
        return cls.instance

    def __init__(self):
        if settings.browser == "chrome":
            options = ChromeOptions()
            # Add headless mode option
            options.add_argument("--headless")
            options.add_argument("--log-level=3")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1920,1080")
            self.driver = webdriver.Chrome(options=options)
        elif settings.browser == "firefox":
            options = FirefoxOptions()
            # Add headless mode option
            options.headless = True
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_argument("--log-level=3")
            self.driver = webdriver.Firefox(options=options)
        else:
            raise Driver.SeleniumDriverNotFound(
                f"{settings.browser} not currently supported")

    def get_driver(self):
        return self.driver

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def navigate(self, url):
        self.driver.get(url)

    def browser_quit(self):
        self.driver.quit()

    def take_screenshot(self, scenario):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        # Create a screenshot filename with the current scenario name and timestamp
        scenario_name = scenario.name.replace(" ", "_")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"{scenario_name}_{timestamp}.png"
        # Take the screenshot and save it to the screenshots directory
        screenshot_path = os.path.join("screenshots", screenshot_filename)
        self.driver.save_screenshot(screenshot_path)


driver = Driver.get_instance()
