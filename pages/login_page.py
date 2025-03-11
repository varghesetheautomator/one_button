import logging
from selenium.webdriver.common.by import By
from context.driver import driver
from selector.login_selectors import LoginPageSelectors as LPS
from selector.home_selectors import HomePageSelectors as HPS
from pages.base_page import Page
from pages.base_page import errors
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.log_utils import Logger
from context.config import settings
import time


log = Logger(__name__, logging.INFO)


class LoginPage(Page):
    """Object to represent the oneButton Login Page"""
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = LoginPage()
        return cls.instance

    def __init__(self):
        super().__init__()

    def get_page_title(self):
        return self.driver.title

    def enter_username(self, username):
        try:
            self.wait_for_selector(LPS.USERNAME)
            self.driver.find_element(
                By.XPATH, LPS.USERNAME).send_keys(username)
            log.logger.info("Username Entered Successfully")
        except Exception as e:
            log.logger.error(
                f"An exception occurred while entering username: {str(e)}")
            errors.append(
                f"An exception occurred while entering username: {str(e)}")
            return errors

    def click_on_next_button(self):
        try:
            self.driver.execute_script(
                f'document.querySelector("{LPS.NEXT_BUTTON_CSS}").click()')
            time.sleep(1)
            error = self.is_displayed_xpath_el(LPS.USERNAME_ERROR)
            if error:
                log.logger.error("Test Failed, Enter a Valid Username")
                errors.append("Test Failed, Enter a Valid Username")
            else:
                self.wait_for_selector(LPS.PASSWORD)
                log.logger.info("Clicked on Next Button Successfully.")
            return errors
        except Exception as e:
            log.logger.error(
                f"An exception occurred while clicking on Next button: {str(e)}")
            errors.append(
                f"An exception occurred while clicking on Next button: {str(e)}")
            return errors

    def enter_password(self, password):
        try:
            self.driver.find_element(By.XPATH, LPS.PASSWORD).clear()
            time.sleep(1)
            self.driver.find_element(
                By.XPATH, LPS.PASSWORD).send_keys(password)
            log.logger.info("Password Entered Successfully.")
        except Exception as e:
            log.logger.error(
                f"An exception occurred while entering password: {str(e)}")
            errors.append(
                f"An exception occurred while entering password: {str(e)}")
            return errors

    def click_on_sign_in_button(self):
        try:
            self.driver.execute_script(
                f'document.querySelector("{LPS.SIGN_BUTTON_CSS}").click()')
            time.sleep(1)
            error = self.is_displayed_xpath_el(LPS.PASSWORD_ERROR)
            if error:
                log.logger.error("Test Failed, Enter a Valid Password")
                errors.append("Test Failed, Enter a Valid Password")
            else:
                self.wait_for_selector(LPS.OK_BUTTON)
                log.logger.info("Clicked on Sign-in Button Successfully.")
        except Exception as e:
            log.logger.error(
                f"An exception occurred while clicking on Sign-in button: {str(e)}")
            errors.append(
                f"An exception occurred while clicking on Sign-in button: {str(e)}")
            return errors

    def click_on_yes_button(self):
        try:
            self.driver.execute_script(
                f'document.querySelector("{LPS.OK_BUTTON_CSS}").click()')
            time.sleep(1)
            self.wait_for_selector(HPS.HOME_SEARCH_ICON)
            log.logger.info("Clicked on Yes Button for Sign-in Successfully.")
        except Exception as e:
            log.logger.error(
                f"An exception occurred while clicking on yes button for Sign-in: {str(e)}")
            errors.append(
                f"An exception occurred while clicking on yes button for Sign-in: {str(e)}")
            return errors

    def error_arr(self):
        return errors
