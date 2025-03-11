from context.driver import driver
import allure
from selenium import webdriver


def after_all(context):
    driver.browser_quit()


def before_scenario(context, scenario):
    driver.clear_cookies()


def before_all(context):
    driver.get_driver()


def after_step(context, step):

    if step.status == 'failed':
        allure.attach(driver.get_driver().get_screenshot_as_png(), name='screenshot',
                      attachment_type=allure.attachment_type.PNG)
