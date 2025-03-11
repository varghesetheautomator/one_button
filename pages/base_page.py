import logging
import random
from selenium.webdriver.support.select import Select
from context.config import settings
from context.driver import Driver, driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selector.home_selectors import HomePageSelectors as HPS
from utils.log_utils import Logger
from selenium.webdriver.support import expected_conditions as EC
from selector.opportunity_selectors import OpportunityPageSelectors as OPS
from selector.system_design_selectors import DesignPageSelectors as SDS
from selector.utility_selectors import UtilityPageSelectors as UPS
from selector.generate_quote_selectors import GenerateQuotePage as GQS
from selector.generate_contract_selectors import GenerateContractPage as GCS
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

errors = []
log = Logger(__name__, logging.INFO)


class Page(Driver):
    """Base class for all page objects in the Page Object Model"""

    def __init__(self):
        self.driver = driver.get_driver()
        self.sys_id = None
        self.idx = None
        self.sys_data_array_battery = []
        self.sys_data_array_roof = []

    def get_sys_id(self, value):
        self.sys_id = value

    def get_idx(self, id):
        self.idx = id

    def get_sys_data_array_battery(self, value):
        self.sys_data_array_battery = None

    def get_sys_data_array_roof(self, value):
        self.sys_data_array_roof = None

    def _execute_with_wait(self, condition):
        return WebDriverWait(self.driver, settings.driver_timeout).until(condition)

    def element_exists(self, locator):
        try:
            self._execute_with_wait(
                ec.presence_of_element_located(
                    (locator))
            )
            return True
        except TimeoutException:
            return False

    def get_element(self, locator):
        if not self.element_exists(locator):
            raise NoSuchElementException("Could not find {locator}")
        return self.driver.find_element(locator)

    def is_displayed_xpath_el(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            status = element.is_displayed()
            return status
        except:
            return False

    def is_displayed_css_el(self, locator):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, locator)
            status = element.is_displayed()
            return status
        except:
            return False

    def wait_for_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return element
        except Exception as e:
            raise e

    def invisibility_for_spinner(self):
        try:
            WebDriverWait(self.driver, 400).until(
                EC.invisibility_of_element((By.XPATH, HPS.SPINNER))
            )
        except TimeoutException:
            raise Exception(
                "PAGE SPINNER is not getting Invisible even after waiting for 400 seconds.")
        except Exception as e:
            raise e

    def invisibility_for_contract_wait_spinner(self):
        try:
            WebDriverWait(self.driver, 300).until(
                EC.invisibility_of_element(
                    (By.XPATH, HPS.CONTRACT_WAIT_SPINNER))
            )
        except TimeoutException:
            raise Exception(
                "CONTRACT WAIT SPINNER is not getting Invisible even after waiting for 300 seconds.")
        except Exception as e:
            raise e

    def wait_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return element
        except:
            return False

    def wait_until_element_is_enabled(self, locator):
        try:
            wait = WebDriverWait(self.driver, 20)
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, locator)))
        except Exception as e:
            log.logger.info(f"An exception occurred: {str(e)}")
            errors.append(f"An exception occurred: {str(e)}")

    def wait_for_selector(self, locator):
        try:
            element = WebDriverWait(self.driver, 80).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
        except TimeoutException:
            raise Exception(
                f"Locator '{locator}' is not visible even after waiting for 80 seconds.")
        except Exception as e:
            raise e

    def wait_for_selector_first_data(self, locator, max_retries=3, retry_interval=5):

        retries = 0
        while retries < max_retries:
            try:
                element = WebDriverWait(self.driver, 80).until(
                    EC.visibility_of_element_located((By.XPATH, locator))
                )
                return element
            except TimeoutException:
                retries += 1
                if retries < max_retries:
                    # print(f"Retrying... Attempt {retries}/{max_retries}")
                    time.sleep(retry_interval)
                else:
                    raise Exception(
                        f"Locator '{locator}' is not visible even after {max_retries} attempts.")
            except Exception as e:
                raise e

    def invisibility_of_alerts(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.invisibility_of_element((By.XPATH, HPS.ALERTS))
            )

        except Exception as e:
            raise e

    def check_dropdown_status(self):
        try:
            time.sleep(2)
            dropdown_status = [
                OPS.OPPORTUNITY_INTEREST_DROP_DOWN_TRUE, OPS.INSTALLATION_ADDRESS_DROP_DOWN_TRUE]
            dropdown = [OPS.OPPORTUNITY_INTEREST_DROPDOWN,
                        OPS.INSTALLATION_ADDRESS_DROPDOWN]
            for i in range(2):
                status = self.is_displayed_xpath_el(dropdown_status[i])
                if status:
                    pass
                else:
                    self.driver.find_element(By.XPATH, dropdown[i]).click()
                    time.sleep(1)
        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")

    def button_click(self, element):
        try:
            locator_type = element[0:2]  # Extract 0th and 1st characters
            if locator_type == "//":
                self.driver.find_element(By.XPATH, element).click()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_of_alerts()
            else:
                self.driver.find_element(By.CSS_SELECTOR, element).click()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_of_alerts()
        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")

    def click_element_with_retry(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.driver.execute_script(
                    f'document.querySelector("{HPS.FIRST_DATA_CSS}").click()')
                return True  # Return True if click is successful
            except Exception as e:
                log.logger.warning(
                    f"Failed to click the element. Retrying... Attempt {attempt+1}/{max_retries}")
                time.sleep(1)  # Adjust wait time as necessary
        log.logger.error(
            "Failed to click the element after multiple attempts.")
        return False  # Return False if click fails after all retries

    def fetch_opportunity(self, opp_id_value):
        try:
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.wait_for_selector(HPS.HOME_SEARCH_FIELD)
            element = self.driver.find_element(By.XPATH, HPS.HOME_SEARCH_FIELD)
            element.send_keys(opp_id_value)
            from_date = self.driver.find_element(By.XPATH, HPS.FROM_DATE)
            from_date.click()
            from_date.clear()
            from_date.send_keys("01-01-2023")
            time.sleep(1)
            self.driver.find_element(By.XPATH, HPS.HOME_SEARCH_ICON).click()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            no_records_found = self.is_displayed_xpath_el(HPS.NO_RECORDS_FOUND)
            if not no_records_found:
                self.wait_for_selector_first_data(HPS.FIRST_DATA)
                time.sleep(1)
                # Retry clicking HPS.FIRST_DATA
                if not self.click_element_with_retry():
                    errors.append(
                        "Failed to click The Opportunity Link after multiple attempts.")
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.wait_for_selector(OPS.OPP_PAGE_VERIFY)
                opp_page_verify = self.is_displayed_xpath_el(
                    OPS.OPP_PAGE_VERIFY)
                if opp_page_verify:
                    log.logger.info(
                        f"Opportunity Page Verified for the opportunity {opp_id_value}...")
                    finance_error = self.is_displayed_xpath_el(
                        OPS.FINANCE_ERROR)
                    if not finance_error:
                        log.logger.info(
                            f"Finance method is selected for the Product by default, Continuing the test for the Opportunity {opp_id_value}")
                    else:
                        log.logger.error(
                            f"Finance method is not selected for the Product by default, Test Failed for the Opportunity {opp_id_value}")
                        errors.append(
                            f"Finance method is not selected for the Product by default, Test Failed for the Opportunity {opp_id_value}")
                else:
                    log.logger.error(
                        f"Opportunity Page Not Verified, Test Failed for the Opportunity {opp_id_value}")
                    errors.append(
                        f"Opportunity Page Not Verified, Test Failed for the Opportunity {opp_id_value}")
            else:
                log.logger.error(
                    f"No Records found for the searched Opportunity : {opp_id_value}")
                errors.append(
                    f"No Records found for the searched Opportunity : {opp_id_value}")
        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")
        return errors

    def opportunity_page_error_validation(self):

        element_list = [OPS.SOLAR_PRODUCT, OPS.ROOF_PRODUCT, OPS.BATTERY_PRODUCT,
                        OPS.RRR_PRODUCT, OPS.FINANCE_SOLAR, OPS.FINANCE_ROOF, OPS.FINANCE_BATTERY, OPS.FINANCE_RRR, OPS.ADD_CONTACT_BTN, OPS.CUSTOMER_INFORMATION_LABEL, OPS.CUST_INFO_FIRST_NAME,
                        OPS.CUST_INFO_LAST_NAME, OPS.CUST_INFO_EMAIL, OPS.CUST_INFO_PHONE, OPS.CUSTOMER_INFORMATION_PHONE_TYPE, OPS.CUSTOMER_INFORMATION_CONTACT_TYPE, OPS.CUSTOMER_INFORMATION_CONTACT_METHOD,
                        OPS.CUSTOMER_INFORMATION_PREFERRED_LANGUAGE, OPS.PRIMARY_CONTACT, OPS.SECONDARY_CONTACT, OPS.ON_UTILITY_BILL, OPS.ADD_TO_CONTRACT, OPS.HOME_OWNER, OPS.ON_TITLE,
                        OPS.GOOGLE_STREET_VIEW, OPS.INSTALLATION_ADDRESS_LABEL, OPS.INSTALLATION_ADDRESS_STREET, OPS.INSTALLATION_ADDRESS_CITY, OPS.INSTALLATION_ADDRESS_STATE, OPS.INSTALLATION_ADDRESS_ZIP_CODE, OPS.INSTALLATION_ADDRESS_LATITUDE,
                        OPS.INSTALLATION_ADDRESS_LONGITUDE, OPS.ACTIVITY_NOTES_BTN]

        element_list_name = ["SOLAR PRODUCT", "ROOF PRODUCT", "BATTERY PRODUCT",
                             "RRR PRODUCT", "FINANCE SOLAR", "FINANCE ROOF", "FINANCE BATTERY", "FINANCE RRR", "ADD CONTACT BUTTON",
                             "CUSTOMER INFORMATION LABEL", "CUSTOMER INFO FIRST NAME", "CUSTOMER INFO LAST NAME",
                             "CUSTOMER INFO EMAIL", "CUSTOMER INFO PHONE", "CUSTOMER INFORMATION PHONE TYPE",
                             "CUSTOMER INFORMATION CONTACT TYPE", "CUSTOMER INFORMATION CONTACT METHOD",
                             "CUSTOMER INFORMATION PREFERRED LANGUAGE", "PRIMARY CONTACT", "SECONDARY CONTACT",
                             "ON UTILITY BILL", "ADD TO CONTRACT", "HOME OWNER", "ON TITLE",
                             "GOOGLE STREET VIEW", "INSTALLATION ADDRESS DROPDOWN", "INSTALLATION ADDRESS STREET",
                             "INSTALLATION ADDRESS CITY", "INSTALLATION ADDRESS STATE", "INSTALLATION ADDRESS ZIP CODE",
                             "INSTALLATION ADDRESS LATITUDE", "INSTALLATION ADDRESS LONGITUDE", "ACTIVITY NOTES BUTTON"
                             ]

        try:
            log.logger.info(
                "Starting Opportunity Page Element Visibility Test for all major elements")
            for i in range(len(element_list)):
                self.wait_for_element((By.XPATH, element_list[i]))
                element = self.is_displayed_xpath_el(element_list[i])
                if not element:
                    errors.append(f" {element_list_name[i]} is not visible")
                    log.logger.error(f" {element_list_name[i]} is not visible")
                else:
                    continue
                    # log.logger.info(f" {element_list_name[i]} is visible")
            log.logger.info(
                "Completed Opportunity Page Element Visibility Test for all major elements")
            time.sleep(2)
            checklist_error = self.is_displayed_xpath_el(OPS.CHECKLIST_ERROR)
            # print(checklist_error)
            if checklist_error:
                log.logger.info(
                    "Error message is showing, Checking the mandatory fields in Opportunity Page for Opportunity")
                card = self.driver.find_elements(
                    By.XPATH, OPS.CUSTOMER_INFORMATION_CARDS)
                lc = len(card)
                for i in range(lc):
                    self.driver.find_element(
                        By.XPATH, OPS.card_len(i + 1)).click()
                    time.sleep(2)
                    f_name_error = self.is_displayed_xpath_el(
                        OPS.FIRST_NAME_MANDATORY_ERROR)
                    l_name_error = self.is_displayed_xpath_el(
                        OPS.LAST_NAME_MANDATORY_ERROR)
                    email_error = self.is_displayed_xpath_el(
                        OPS.EMAIL_MANDATORY_ERROR)
                    ph_no_error = self.is_displayed_xpath_el(
                        OPS.PHONE_NUMBER_MANDATORY_ERROR)
                    if not f_name_error and not l_name_error:
                        log.logger.info(
                            f"Mandatory First/Last name field is not null for contact {i + 1}, Test can be continued!")
                        if email_error:
                            log.logger.info(
                                f"Email field is null for contact {i + 1}, entering value...")
                            name = self.driver.find_element(
                                By.XPATH, OPS.CUST_INFO_FIRST_NAME).get_attribute("value")
                            mail_id = name.casefold() + "@gmail.com"
                            mail_type_field = self.driver.find_element(
                                By.XPATH, OPS.CUST_INFO_EMAIL)
                            mail_type_field.send_keys(mail_id)
                            log.logger.info(
                                f"Email entered successfully for contact {i + 1}")
                        if ph_no_error:
                            log.logger.info(
                                f"Phone number field is null for contact {i + 1}, entering value...")
                            ph = self.driver.find_element(
                                By.XPATH, OPS.CUST_INFO_PHONE)
                            ph_value = random.randrange(10 ** 9, 10 ** 10)
                            ph.send_keys(ph_value)
                            log.logger.info(
                                f"Phone number entered successfully for contact {i + 1}")
                    else:
                        log.logger.error(
                            f"Test failed !! Mandatory First/Last name field for contact {i + 1} is null, Test cannot be continued!")
                        errors.append(
                            f"Test failed !! Mandatory First/Last name field for contact {i + 1} is null, Test cannot be continued!")
                        break
            else:
                log.logger.info(
                    "No errors are identified, Mandatory field validation completed for Opportunity Page")
        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")
        return errors

    def check_product_and_fin_method(self, opp_id):
        try:
            solar_cb = self.is_displayed_xpath_el(OPS.SOLAR_SELECTED)
            roof_cb = self.is_displayed_xpath_el(OPS.ROOF_SELECTED)
            battery_cb = self.is_displayed_xpath_el(OPS.BATTERY_SELECTED)
            rrr_cb = self.is_displayed_xpath_el(OPS.RRR_SELECTED)
            finance_solar = self.driver.find_element(
                By.XPATH, OPS.FINANCE_SOLAR)
            finance_roof = self.driver.find_element(
                By.XPATH, OPS.FINANCE_ROOF)
            finance_battery = self.driver.find_element(
                By.XPATH, OPS.FINANCE_BATTERY)
            finance_rrr = self.driver.find_element(
                By.XPATH, OPS.FINANCE_RRR)
# tc_01*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Page":
                select = Select(finance_solar)
                selected_option = select.first_selected_option.text
                time.sleep(1)
                if solar_cb and selected_option == "Sunnova":
                    log.logger.info(
                        f"Solar is selected as Product for the Opportunity ID:{opp_id} with Finance as :{selected_option}")
                    if roof_cb or battery_cb or rrr_cb:
                        log.logger.error(
                            f"Products other than Solar is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar")
# tc_02*******************************************************************************************************#
            if self.__class__.__name__ == "Roof_Sunnova_Page":
                select = Select(finance_roof)
                selected_option = select.first_selected_option.text
                if roof_cb and selected_option == "Sunnova":
                    log.logger.info(
                        f"Roof is selected as Product for the Opportunity ID:{opp_id} with Finance as :{selected_option}")
                    if solar_cb or battery_cb or rrr_cb:
                        log.logger.error(
                            f"Products other than Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} , which the product should Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} , which the product should Roof")
# tc_03*******************************************************************************************************#
            if self.__class__.__name__ == "Roof_Cash_Page":
                select = Select(finance_roof)
                selected_option = select.first_selected_option.text
                if roof_cb and selected_option == "Cash":
                    log.logger.info(
                        f"Roof is selected as Product for the Opportunity ID:{opp_id} with Finance as :{selected_option}")
                    if solar_cb or rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} which the product should Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} which the product should Roof")
# tc_04*******************************************************************************************************#
            if self.__class__.__name__ == "Battery_Cash_Page":
                select = Select(finance_battery)
                selected_option = select.first_selected_option.text
                if battery_cb and selected_option == "Cash":
                    log.logger.info(
                        f"Battery is selected as Product for the Opportunity ID:{opp_id} with Finance as :{selected_option}")
                    if solar_cb or rrr_cb or roof_cb:
                        log.logger.error(
                            f"Products other than Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}  which the product should Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}  which the product should Battery")
# tc_05*******************************************************************************************************#
            if self.__class__.__name__ == "RRR_Sunnova_Page":
                select = Select(finance_rrr)
                selected_option = select.first_selected_option.text
                if rrr_cb and selected_option == "Sunnova":
                    log.logger.info(
                        f"RRR is selected as Product for the Opportunity ID:{opp_id} with Finance as :{selected_option}")
                    if solar_cb or battery_cb or roof_cb:
                        log.logger.error(
                            f"Products other than RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}  which the product should RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}  which the product should RRR")
# tc_06*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Sunnova" and selected_option_roof == "Sunnova":
                    log.logger.info(
                        f"Solar and Roof is selected as Product with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} , which the product should Solar & Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} , which the product should Solar & Roof")
# tc_07*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb:
                    log.logger.info(
                        f"Solar,Roof is selected as Product with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb and selected_option_solar == "Sunnova" and selected_option_roof == "Cash":
                        log.logger.error(
                            f"Products other than Solar,Roof is selected this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof is selected this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} , which the product should Solar & Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id} , which the product should Solar & Roof")
# tc_08*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb or roof_cb:
                        log.logger.error(
                            f"Products other than Solar,Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar & Battery")
# tc_09*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)

                if solar_cb and rrr_cb and selected_option_solar == "Sunnova" and selected_option_rrr == "Sunnova":
                    log.logger.info(
                        f"Solar and RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar & RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar & RRR")
# tc_10*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Cash_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_roof == "Cash" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery}  for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, Roof & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, Roof & Battery")
# tc_11*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Sunnova_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)

                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_roof == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery}  for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, Roof & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, Roof & Battery")
# tc_12*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Cash_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_rrr == "Cash" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,RRR and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, RRR & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, RRR & Battery")
# tc_13*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Cash" and selected_option_roof == "Cash":
                    log.logger.info(
                        f"Solar,Roof is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof")
# tc_14*******************************************************************************************************#
            if self.__class__.__name__ == "Roof_Cash_Battery_Cash_Page":
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if roof_cb and battery_cb and selected_option_roof == "Cash" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Roof,Battery is selected as Products with Finance as :{selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb or solar_cb:
                        log.logger.error(
                            f"Products other than Roof,Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Roof,Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Roof,Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Roof,Battery")
# tc_15*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Cash" and selected_option_rrr == "Cash":
                    log.logger.info(
                        f"Solar,RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR")
# tc_16*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Sunnova_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Cash" and selected_option_roof == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, Roof & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, Roof & Battery")
# tc_17*******************************************************************************************************#
            if self.__class__.__name__ == "RRR_Cash_Page":
                select = Select(finance_rrr)
                selected_option = select.first_selected_option.text
                if rrr_cb and selected_option == "Cash":
                    log.logger.info(
                        f"RRR is selected as Product with Finance as :{selected_option} for the Opportunity ID:{opp_id}")
                    if solar_cb or roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Roof")
# tc_18*******************************************************************************************************#
            if self.__class__.__name__ == "Rrr_Service_Finance_Page":
                select = Select(finance_rrr)
                selected_option = select.first_selected_option.text
                # print(selected_option)
                if rrr_cb and selected_option == "Service Finance":
                    log.logger.info(
                        f"RRR is selected as Product with Finance as :{selected_option} for the Opportunity ID:{opp_id}")
                    if solar_cb or roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should RRR")
# tc_19*******************************************************************************************************#
            if self.__class__.__name__ == "Roof_Service_Finance_Page":
                select = Select(finance_roof)
                selected_option = select.first_selected_option.text
                # print(selected_option)
                if roof_cb and selected_option == "Service Finance":
                    log.logger.info(
                        f"Roof is selected as Product with Finance as :{selected_option} for the Opportunity ID:{opp_id}")
                    if solar_cb or rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Roof")
# tc_20*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Page":
                select = Select(finance_solar)
                selected_option = select.first_selected_option.text
                time.sleep(1)
                if solar_cb and selected_option == "Cash":
                    log.logger.info(
                        f"Solar is selected as Product with Finance as :{selected_option} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb or rrr_cb:
                        log.logger.error(
                            f"Products other than Solar is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar")
# tc_21*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Cash" and selected_option_roof == "Sunnova":
                    log.logger.info(
                        f"Solar and Roof is selected as Product with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Roof")
# tc_22*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Sunnova" and selected_option_rrr == "Cash":
                    log.logger.info(
                        f"Solar,RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar, RRR")
# tc_23*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Page":
                select = Select(finance_solar)
                selected_option = select.first_selected_option.text
                time.sleep(1)
                if solar_cb and selected_option == "Service Finance":
                    log.logger.info(
                        f"Solar is selected as Product with Finance as :{selected_option} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb or rrr_cb:
                        log.logger.error(
                            f"Products other than Solar is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Solar")
# tc_24*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_service_finance_Rrr_service_finance_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Service Finance" and selected_option_rrr == "Service Finance":
                    log.logger.info(
                        f"Solar,RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR with Finance as Service Finance")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR with Finance as Service Finance")
# tc_25*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Cash_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Cash" and selected_option_roof == "Cash" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_26*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_service_finance_Roof_service_finance_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Service Finance" and selected_option_roof == "Service Finance":
                    log.logger.info(
                        f"Solar,Roof is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof with Finance as Service Finance")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof with Finance as Service Finance")
# tc_27*******************************************************************************************************#
            if self.__class__.__name__ == "Roof_Sunnova_Battery_Cash_Page":
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)

                if roof_cb and battery_cb and selected_option_roof == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Roof and Battery is selected as Products with Finance as :{selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb or solar_cb:
                        log.logger.error(
                            f"Products other than Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Roof & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Roof & Battery")
# tc_28*******************************************************************************************************#
            if self.__class__.__name__ == "Roof_Service_Finance_Battery_Cash_Page":
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if roof_cb and battery_cb and selected_option_roof == "Service Finance" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Roof and Battery is selected as Products with Finance as :{selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb or solar_cb:
                        log.logger.error(
                            f"Products other than Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Roof and Battery with Finance method as Service Finance and Cash")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Roof and Battery with Finance method as Service Finance and Cash")
# tc_29*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and battery_cb and selected_option_solar == "Cash" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb or roof_cb:
                        log.logger.error(
                            f"Products other than Solar and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar & Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar & Battery")
# tc_30*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Service_Finance_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Sunnova" and selected_option_roof == "Service Finance":
                    log.logger.info(
                        f"Solar,Roof is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof")
# tc_31*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb or roof_cb:
                        log.logger.error(
                            f"Products other than Solar and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Battery with Finance method as Service Finance and Cash")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Battery with Finance method as Service Finance and Cash")
# tc_32*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_service_finance_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Cash" and selected_option_roof == "Service Finance":
                    log.logger.info(
                        f"Solar,Roof is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof")
# tc_33*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Service Finance" and selected_option_roof == "Sunnova":
                    log.logger.info(
                        f"Solar and Roof is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and Roof is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and Roof is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Roof")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Roof")
# tc_34*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and selected_option_solar == "Service Finance" and selected_option_roof == "Cash":
                    log.logger.info(
                        f"Solar and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Battery with Finance method as Service Finance and Cash")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and Battery with Finance method as Service Finance and Cash")
# tc_35*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Service_Finance_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Sunnova" and selected_option_rrr == "Service Finance":
                    log.logger.info(
                        f"Solar,RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR")
# tc_36*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_RRR_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Cash" and selected_option_rrr == "Sunnova":
                    log.logger.info(
                        f"Solar and RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and RRR")
# tc_37*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_RRR_service_finance_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Cash" and selected_option_rrr == "Service Finance":
                    log.logger.info(
                        f"Solar,RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR")
# tc_38*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_RRR_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Service Finance" and selected_option_rrr == "Sunnova":
                    log.logger.info(
                        f"Solar and RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar and RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar and RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and RRR")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar and RRR")
# tc_39*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_service_finance_Rrr_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and selected_option_solar == "Service Finance" and selected_option_rrr == "Cash":
                    log.logger.info(
                        f"Solar,RRR is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb or battery_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR with Finance as Service Finance")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR with Finance as Service Finance")
# tc_40*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Service_Finance_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Cash" and selected_option_roof == "Service Finance" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery as Products with Finance as :{selected_option_solar} and {selected_option_roof} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_41*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Service_Finance_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_roof == "Service Finance" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar, Roof and Battery as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_42*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Sunnova_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_roof == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_43*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Cash_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_roof == "Cash" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_44*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Service_Finance_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_roof = Select(finance_roof)
                selected_option_roof = select_roof.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and roof_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_roof == "Service Finance" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_roof} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if rrr_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_45*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Sunnova_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_rrr == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_46*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Cash_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Cash" and selected_option_battery == "Cash" and selected_option_rrr == "Cash":
                    log.logger.info(
                        f"Solar,RRR and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} and {selected_option_rrr} for the Opportunity ID:{opp_id}")

                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
# tc_47*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Service_Finance_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Cash" and selected_option_battery == "Cash" and selected_option_rrr == "Service Finance":
                    log.logger.info(
                        f"Solar,RRR and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
# tc_48*******************************************************************************************************
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Service_Finance_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_rrr == "Service Finance" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,RRR and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
# tc_49*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Sunnova_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Cash" and selected_option_rrr == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_50*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Rrr_Cash_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_battery == "Cash" and selected_option_rrr == "Cash":
                    log.logger.info(
                        f"Solar,RRR and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
# tc_51*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Rrr_Service_Finance_Battery_Cash":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_battery == "Cash" and selected_option_rrr == "Service Finance":
                    log.logger.info(
                        f"Solar,RRR and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} and {selected_option_rrr} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,RRR and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,RRR and Battery")
# tc_52*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Rrr_Sunnova_Battery_Cash_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select_rrr = Select(finance_rrr)
                selected_option_rrr = select_rrr.first_selected_option.text
                time.sleep(1)
                select_battery = Select(finance_battery)
                selected_option_battery = select_battery.first_selected_option.text
                time.sleep(1)
                if solar_cb and rrr_cb and battery_cb and selected_option_solar == "Service Finance" and selected_option_rrr == "Sunnova" and selected_option_battery == "Cash":
                    log.logger.info(
                        f"Solar,Roof and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_rrr} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if roof_cb:
                        log.logger.error(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Solar,Roof and Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should"
                        " be Solar,Roof and Battery")
# tc_53*******************************************************************************************************#
            if self.__class__.__name__ == "Battery_Sunnova":
                select = Select(finance_battery)
                selected_option = select.first_selected_option.text
                time.sleep(1)
                if battery_cb and selected_option == "Sunnova":
                    log.logger.info(
                        f"Battery is selected as Products with Finance as :{selected_option} for the Opportunity ID:{opp_id}")
                    if roof_cb or solar_cb or rrr_cb:
                        log.logger.error(
                            f"Products other than Battery is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Battery is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should Battery")
# tc_54*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Battery_Sunnova_Page":
                select_solar = Select(finance_solar)
                selected_option_solar = select_solar.first_selected_option.text
                time.sleep(1)
                select = Select(finance_battery)
                selected_option_battery = select.first_selected_option.text
                time.sleep(1)
                if solar_cb and battery_cb and selected_option_solar == "Sunnova" and selected_option_battery == "Sunnova":
                    log.logger.info(
                        f"Solar and Battery is selected as Products with Finance as :{selected_option_solar} and {selected_option_battery} for the Opportunity ID:{opp_id}")
                    if roof_cb or rrr_cb:
                        log.logger.error(
                            f"Products other than Battery and Solar is selected for this Opportunity: {opp_id}")
                        errors.append(
                            f"Products other than Battery and Solar is selected for this Opportunity: {opp_id}")
                else:
                    log.logger.error(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should be Solar and Battery")
                    errors.append(
                        f"Pre-Requisites is not satisfied this Opportunity: {opp_id}, which the product should be Solar and Battery")
# ************************************************************************************************************#
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def check_create_lead_id(self):
        try:
            time.sleep(1)
            finance_solar = self.driver.find_element(
                By.XPATH, OPS.FINANCE_SOLAR)
            finance_roof = self.driver.find_element(By.XPATH, OPS.FINANCE_ROOF)
            finance_battery = self.driver.find_element(
                By.XPATH, OPS.FINANCE_BATTERY)
            finance_rrr = self.driver.find_element(By.XPATH, OPS.FINANCE_RRR)
            select_solar = Select(finance_solar)
            selected_option_solar = select_solar.first_selected_option.text
            select_roof = Select(finance_roof)
            selected_option_roof = select_roof.first_selected_option.text
            select_battery = Select(finance_battery)
            selected_option_battery = select_battery.first_selected_option.text
            select_rrr = Select(finance_rrr)
            selected_option_rrr = select_rrr.first_selected_option.text

            # print(selected_option_solar, selected_option_roof,
            #       selected_option_battery, selected_option_rrr)
            if selected_option_solar == "Sunnova":
                solar_lead_id = self.is_displayed_xpath_el(OPS.SOLAR_LEAD_ID)
                if solar_lead_id:
                    log.logger.info(
                        "Finance Partner Contact ID is present for Solar with Sunnova as Finance method")
                else:
                    log.logger.error(
                        "Finance Partner Contact ID is not present for Solar with Sunnova as Finance method, "
                        "even the opportunity is synced")
                    errors.append(
                        "Finance Partner Contact ID is not present for Solar with Sunnova as Finance method, "
                        "even the opportunity is synced")
            else:
                pass
            if selected_option_roof == "Sunnova":
                roof_lead_id = self.is_displayed_xpath_el(OPS.ROOF_LEAD_ID)
                if roof_lead_id:
                    log.logger.info(
                        "Finance Partner Contact ID is present for Roof with Sunnova as Finance method")
                else:
                    log.logger.error(
                        "Finance Partner Contact ID is not present for Roof with Sunnova as Finance method, even the opportunity is synced")
                    errors.append(
                        "Finance Partner Contact ID is not present for Roof with Sunnova as Finance method, even the opportunity is synced")
            else:
                pass
            if selected_option_battery == "Sunnova":
                battery_lead_id = self.is_displayed_xpath_el(
                    OPS.BATTERY_LEAD_ID)
                if battery_lead_id:
                    log.logger.info(
                        "Finance Partner Contact ID is present for Battery with Sunnova as Finance method")
                else:
                    log.logger.error(
                        "Finance Partner Contact ID is not present for Battery with Sunnova as Finance method, even the opportunity is synced")
                    errors.append(
                        "Finance Partner Contact ID is not present for Battery with Sunnova as Finance method, even the opportunity is synced")
            else:
                pass
            if selected_option_rrr == "Sunnova":
                rrr_lead_id = self.is_displayed_xpath_el(OPS.RRR_LEAD_ID)
                if rrr_lead_id:
                    log.logger.info(
                        "Finance Partner Contact ID is present for RRR with Sunnova as Finance method")
                else:
                    log.logger.error(
                        "Finance Partner Contact ID is not present for RRR with Sunnova as Finance method, even the opportunity is synced")
                    errors.append(
                        "Finance Partner Contact ID is not present for RRR with Sunnova as Finance method, even the opportunity is synced")
            else:
                pass
        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")
        return errors

    def sunnova_sync(self):
        try:
            sunnova_sync = self.is_displayed_xpath_el(OPS.SUNNOVA_SYNCED_BTN)
            if sunnova_sync:
                self.check_create_lead_id()
            else:
                sunnova_un_sync = self.is_displayed_xpath_el(
                    OPS.SUNNOVA_UN_SYNCED)
                if sunnova_un_sync:
                    log.logger.info(
                        "Opportunity is Not Synced, Continuing to Sync the Opportunity")
                    un_sync_btn = self.driver.find_element(
                        By.XPATH, OPS.SUNNOVA_UN_SYNCED)
                    un_sync_btn.click()
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(2)
                    lead_not_found = self.is_displayed_xpath_el(
                        OPS.LEAD_NOT_FOUND_ERROR)
                    # print(lead_not_found)
                    time.sleep(1)
                    if lead_not_found:
                        create_new_lead = self.driver.find_element(
                            By.XPATH, OPS.CREATE_NEW_SUNNOVA_LEAD_BTN)
                        create_new_lead.click()
                        time.sleep(1)
                    else:
                        chk_box = self.is_displayed_xpath_el(
                            OPS.CHECK_BOX_SYNC_POP_UP)
                        if chk_box:
                            chk_select = self.driver.find_element(
                                By.XPATH, OPS.CHECK_BOX_SYNC_POP_UP).is_selected()
                            if not chk_select:
                                self.driver.find_element(
                                    By.XPATH, OPS.CHECK_BOX_SYNC_POP_UP).click()
                            else:
                                pass
                            sync_btn = self.driver.find_element(
                                By.XPATH, OPS.SYNC_BUTTON_SUNNOVA_LEAD)
                            sync_btn.click()
                            time.sleep(2)
                            pop_up = self.is_displayed_xpath_el(
                                OPS.ADDRESS_MISMATCH_POPUP)
                            # print(pop_up)
                            if pop_up:
                                self.driver.find_element(
                                    By.XPATH, OPS.ADDRESS_MISMATCH_POPUP_OK).click()
                            else:
                                self.invisibility_for_spinner()
                                pass
                        else:
                            pass
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    failed = self.is_displayed_xpath_el(OPS.SUNNOVA_FAILED)
                    pending = self.is_displayed_xpath_el(OPS.SUNNOVA_PENDING)
                    if not failed or not pending:
                        success = self.is_displayed_xpath_el(
                            OPS.SUNNOVA_SUCCESSFUL)
                        if success:
                            self.driver.find_element(
                                By.XPATH, OPS.CLOSE_POPUP).click()
                            time.sleep(3)
                            self.opportunity_page_error_validation()
                            self.check_create_lead_id()
                        else:
                            errors.append(
                                "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                            log.logger.error(
                                "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                    else:
                        errors.append(
                            "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                        log.logger.error(
                            "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                else:
                    log.logger.info(
                        "Opportunity is Sunnova Sync button is not visible")

        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def black_knight_sync(self):
        try:
            log.logger.info(
                "Started Checking if the Opportunity is Synced or Not")
            black_un_sync = self.is_displayed_xpath_el(OPS.BLACK_KNIGHT_SYNCED)
            if black_un_sync:
                log.logger.info(
                    "Opportunity is Not Black Knight Synced, Continuing to Sync the Opportunity")
                un_sync_btn = self.driver.find_element(
                    By.XPATH, OPS.BLACK_KNIGHT_SYNCED)
                un_sync_btn.click()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                lead_not_found = self.is_displayed_xpath_el(
                    OPS.LEAD_NOT_FOUND_BLACK_KNIGHT)
                if lead_not_found:
                    close = self.driver.find_element(By.XPATH, OPS.CLOSE_POPUP)
                    close.click()
                else:
                    sync_btn = self.driver.find_element(
                        By.XPATH, OPS.BLACK_KNIGHT_SYNC_SYNCING)
                    sync_btn.click()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
            else:
                log.logger.info(
                    "Opportunity is Black Knight Synced, Continuing the Test")
            self.opportunity_page_error_validation()

        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def sync_error_popup(self):
        try:
            sync_error = self.is_displayed_xpath_el(
                GCS.CONTRACT_PAGE_SYNC_ERROR)
            if sync_error:
                close = self.is_displayed_xpath_el(
                    GCS.CLOSE_ERROR)
                if close:
                    close = self.driver.find_element(
                        By.XPATH, GCS.CLOSE_ERROR)
                    close.click()
                    time.sleep(2)
            else:
                pass
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

    def sync_error_close(self):
        try:
            sync_error = self.is_displayed_xpath_el(
                SDS.SYNC_STATUS_POP_UP)
            if sync_error:
                close = self.is_displayed_xpath_el(
                    GCS.CLOSE_ERROR)
                if close:
                    close = self.driver.find_element(
                        By.XPATH, GCS.CLOSE_ERROR)
                    close.click()
                    time.sleep(2)
                else:
                    pass
            else:
                pass
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

    def utility_page(self):
        try:
            log.logger.info("Started Utility Page Error Validation...")
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(2)
            page_verify = self.is_displayed_xpath_el(
                UPS.UTILITY_INFORMATION_TEXT)
            if page_verify:
                utility_bill_select = self.is_displayed_xpath_el(
                    UPS.UTILITY_BILL_NOT_SELECTED)
                if not utility_bill_select:
                    annual_usage_error = self.is_displayed_xpath_el(
                        UPS.ANNUAL_USAGE_ERROR)
                    if annual_usage_error:
                        annual_usage = self.driver.find_element(
                            By.XPATH, UPS.ANNUAL_USAGE_INPUT)
                        annual_usage.clear()
                        annual_usage.send_keys("25000")
                    else:
                        pass
                    log.logger.info(
                        "Completed Error Validation in Utility Page.")
                    self.invisibility_for_spinner()
                    time.sleep(2)
                    self.invisibility_of_alerts()
                    self.button_click(OPS.SAVE)
                    log.logger.info("Entering to Load Calculator section...")
                    time.sleep(2)
                    self.button_click(UPS.LOAD_CALC_TAB)
                    self.button_click(OPS.SAVE)
                    input_fields = self.driver.find_elements(
                        By.XPATH, UPS.LOAD_ITEMS_COUNT)
                    # print(len(input_fields))
                    for i in range(len(input_fields)):
                        input_field = self.driver.find_element(
                            By.XPATH, UPS.load_calc_input(i + 1))
                        input_field.send_keys(
                            Keys.BACKSPACE * len(input_field.get_attribute('value')))
                    time.sleep(1)

                    for i in range(10):
                        input_field = self.driver.find_element(
                            By.XPATH, UPS.load_calc_input(i + 1))
                        input_field.send_keys(2)
                    est_annual_usage = self.driver.find_element(
                        By.XPATH, UPS.EST_ANNUAL_USAGE).text
                    # print(est_annual_usage)
                    if est_annual_usage == "4,992":
                        log.logger.info(
                            "The Estimated Annual Usage time is populated correctly inside Load Calculator,Test Passed!!")
                    else:
                        errors.append(
                            "Test Failed!!,The Estimated Annual Usage time is not populated correctly inside Load Calculator")
                        log.logger.error(
                            "Test Failed!!,The Estimated Annual Usage time is not populated correctly inside Load Calculator")
                    log.logger.info("Saving the Utility Page.")
                    self.button_click(OPS.SAVE)
                    self.button_click(OPS.NEXT)
                else:
                    errors.append(
                        "Test Failed!!,Utility Bill Not Selected for any contact in Opportunity Page")
                    log.logger.error(
                        "Test Failed!!,Utility Bill Not Selected for any contact in Opportunity Page")
            else:
                errors.append("Test Failed!!,Utility Page Not Verified")
                log.logger.error("Test Failed!!,Utility Page Not Verified")
            log.logger.info("Completed Utility Page Functionality...")
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def sys_design_solar(self):
        try:
            sys_design_array = self.is_displayed_xpath_el(SDS.SYS_DESIGN_ARRAY)
            if sys_design_array:
                self.sync_error_close()
                log.logger.info(
                    "At least One Array Card is present in System Design Page, Test can be continued")
                system_size = self.driver.find_element(
                    By.XPATH, SDS.SYSTEM_SIZE)
                system_size_text = system_size.text
                if system_size_text is not None and system_size_text != "":
                    log.logger.info(
                        "System Design Data Available, Continuing the Test..")
                    self.button_click(OPS.SAVE)
                    time.sleep(1)
                    self.sync_error_popup()
                    time.sleep(1)
                    self.sync_error_popup()
                else:
                    errors.append(
                        "Test Failed!!System Design Data Not Available for the Opportunity")
                    log.logger.error(
                        "Test Failed!!System Design Data Not Available for the Opportunity")
            else:
                errors.append(
                    "Test Failed!!No Cards found in System design for the Opportunity")
                log.logger.error(
                    "Test Failed!!No Cards found in System design for the Opportunity")
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def sys_design_roof(self):
        try:
            self.invisibility_for_spinner()
            time.sleep(2)
            roof_tab = self.driver.find_element(By.XPATH, SDS.DESIGN_ROOF_TAB)
            roof_tab.click()
            time.sleep(2)
            self.invisibility_for_spinner()
            time.sleep(3)
            self.sync_error_close()
            manufacturer = Select(self.driver.find_element(
                By.XPATH, SDS.MANUFACTURER_ID_SELECT))
            manufacturer.select_by_index(1)
            time.sleep(2)
            self.invisibility_for_spinner()
            roof_product = Select(self.driver.find_element(
                By.XPATH, SDS.MANUFACTURER_ID_SELECT))
            roof_product.select_by_index(1)
            time.sleep(2)
            roof_manufacturer = Select(
                self.driver.find_element(By.XPATH, SDS.ROOF_MANUFACTURER))
            roof_manufacturer_val = roof_manufacturer.first_selected_option.text
            time.sleep(1)
            roof_prod = Select(self.driver.find_element(
                By.XPATH, SDS.ROOF_PRODUCT))
            roof_prod_val = roof_prod.first_selected_option.text
            self.invisibility_for_spinner()
            roof_sq_override = self.driver.find_element(
                By.XPATH, SDS.ROOF_SQUARE_OVERRIDE_FIELD)
            roof_sq_override.clear()
            roof_sq_override.send_keys("10")
            time.sleep(2)
            roof_sq = self.driver.find_element(
                By.XPATH, SDS.ROOF_SQUARE_OVERRIDE_FIELD).get_attribute("value")

            self.sys_data_array_roof.append(
                [roof_manufacturer_val, roof_prod_val, roof_sq])

            self.button_click(OPS.SAVE)
            self.sync_error_popup()
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def sys_design_rrr(self):
        try:
            rrr_tab = self.driver.find_element(By.XPATH, SDS.DESIGN_RRR_TAB)
            rrr_tab.click()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.sync_error_close()
            time.sleep(3)
            manufacturer = Select(self.driver.find_element(
                By.XPATH, SDS.MANUFACTURER_ID_SELECT))
            manufacturer.select_by_index(1)
            time.sleep(2)
            roof_product = Select(self.driver.find_element(
                By.XPATH, SDS.MANUFACTURER_ID_SELECT))
            roof_product.select_by_index(1)
            time.sleep(1)
            roof_manufacturer = Select(
                self.driver.find_element(By.XPATH, SDS.ROOF_MANUFACTURER))
            roof_manufacturer_val = roof_manufacturer.first_selected_option.text
            roof_prod = Select(self.driver.find_element(
                By.XPATH, SDS.ROOF_PRODUCT))
            roof_prod_val = roof_prod.first_selected_option.text
            time.sleep(1)
            roof_sq_override = self.driver.find_element(
                By.XPATH, SDS.ROOF_SQUARE_OVERRIDE_FIELD)
            roof_sq_override.clear()
            roof_sq_override.send_keys("10")
            time.sleep(1)
            rrr_system_size = self.driver.find_element(
                By.XPATH, SDS.RRR_SYSTEM_SIZE)
            rrr_system_size.clear()
            rrr_system_size.send_keys("10.00")
            time.sleep(1)
            roof_sq = self.driver.find_element(
                By.XPATH, SDS.ROOF_SQUARE_OVERRIDE_FIELD).get_attribute("value")
            self.sys_data_array_roof.append(
                [roof_manufacturer_val, roof_prod_val, roof_sq])

            self.button_click(OPS.SAVE)
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def sys_design_battery(self):
        try:
            self.invisibility_for_spinner()
            time.sleep(2)
            battery_tab = self.driver.find_element(
                By.XPATH, SDS.DESIGN_BATTERY_TAB)
            battery_tab.click()
            time.sleep(2)
            self.invisibility_for_spinner()
            time.sleep(3)
            battery_error = self.is_displayed_xpath_el(SDS.BATTERY_TAB_ERROR)
            if battery_error:
                battery_manufacturer = Select(
                    self.driver.find_element(By.XPATH, SDS.BATTERY_MANUFACTURER))
                battery_manufacturer.select_by_value("Tesla")
                self.invisibility_for_spinner()
                time.sleep(1)
                battery_manufacturer_name = Select(
                    self.driver.find_element(By.XPATH, SDS.BATTERY_MANUFACTURER_NAME))
                battery_manufacturer_name.select_by_visible_text(
                    "Tesla Powerwall")
                self.invisibility_for_spinner()
                time.sleep(1)
                battery_quantity = Select(
                    self.driver.find_element(By.XPATH, SDS.BATTERY_QUANTITY))
                battery_quantity.select_by_value("2")
                self.invisibility_for_spinner()
            else:
                log.logger.info("Battery information is already entered")
            battery_manufacturer = Select(
                self.driver.find_element(By.XPATH, SDS.BATTERY_MANUFACTURER))
            battery_manufacturer_val = battery_manufacturer.first_selected_option.text
            battery_quantity = Select(
                self.driver.find_element(By.XPATH, SDS.BATTERY_QUANTITY))
            battery_quantity_val = battery_quantity.first_selected_option.text
            self.sys_data_array_battery.append(
                [battery_manufacturer_val, battery_quantity_val])
            self.button_click(OPS.SAVE)
            self.sync_error_popup()

        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def system_design(self):
        try:
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.sync_error_close()
            solar_tab = self.is_displayed_xpath_el(SDS.DESIGN_SOLAR_TAB)
            roof_tab = self.is_displayed_xpath_el(SDS.DESIGN_ROOF_TAB)
            battery_tab = self.is_displayed_xpath_el(SDS.DESIGN_BATTERY_TAB)
            rrr_tab = self.is_displayed_xpath_el(SDS.DESIGN_RRR_TAB)
            # print("self.__class__.__name__", self.__class__.__name__)
    # tc_01*******************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Page":
                if all([solar_tab, not roof_tab, not battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly showing only Solar for Solar Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar Sunnova Product, Continuing the Test")
                        self.sys_design_solar()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Solar only for Solar Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Solar only for Solar Sunnova Product,Kindly recheck")
    # tc_02*******************************************************************************************************#
            elif self.__class__.__name__ == "Roof_Sunnova_Page":
                if all([roof_tab, not solar_tab, not battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof, for Roof Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_ROOF)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Roof Sunnova Product, Continuing the Test")
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Roof Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Roof Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Roof Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Roof Sunnova Product,Kindly recheck")
    # tc_03*******************************************************************************************************#
            elif self.__class__.__name__ == "Roof_Cash_Page":
                if all([roof_tab, not solar_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof,for Roof Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_ROOF)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Roof Cash Product,Continuing the Test")
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Roof Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Roof Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Roof Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Roof Cash Product,Kindly recheck")
    # tc_04*******************************************************************************************************#
            elif self.__class__.__name__ == "Battery_Cash_Page":
                if all([battery_tab, not solar_tab, not rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof for Battery Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_BATTERY)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Battery Cash Product , Continuing the Test")
                        self.sys_design_battery()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Battery Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Battery Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Battery Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Battery Cash Product,Kindly recheck")
    # tc_05*******************************************************************************************************#
            elif self.__class__.__name__ == "RRR_Sunnova_Page":
                if all([rrr_tab, not solar_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof for RRR Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_ROOF)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for RRR Sunnova Product , Continuing the Test")
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for RRR Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for RRR Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for RRR Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for RRR Sunnova Product,Kindly recheck")
    # tc_06*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Roof_Sunnova_Page":
                if all([roof_tab, solar_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Roof-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Roof-Sunnova Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Sunnova Product Kindly recheck")
    # tc_07*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Roof_Cash_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Roof-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified  for Solar-Sunnova and Roof-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified  for Solar-Sunnova and Roof-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Cash Product Kindly recheck")
    # tc_08*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Battery_Cash_Page":
                if all([solar_tab, battery_tab, not rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Battery-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Battery-Cash Product,Kindly recheck")
    # tc_09*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_RRR_Sunnova_Page":
                if all([rrr_tab, solar_tab, not roof_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and RRR-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and RRR-Sunnova Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Sunnova Product,Kindly recheck")
    # tc_10*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Roof_Cash_Battery_Cash_Page":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Roof-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Roof-Cash and Battery-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Cash and Battery-Cash Product,Kindly recheck")
    # tc_11*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Roof_Sunnova_Battery_Cash_Page":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Roof-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Roof-Sunnova and Battery-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Sunnova and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Sunnova and Battery-Cash Product,Kindly recheck")
    # tc_12*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_RRR_Cash_Battery_Cash_Page":
                if all([rrr_tab, solar_tab, battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and RRR-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and RRR-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Cash and Battery-Cash Product,Kindly recheck")
    # tc_13*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Roof_Cash_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Roof-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified , Continuing the Test for Solar-Cash and Roof-Cash Product")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Cash Product,Kindly recheck")
    # tc_14*******************************************************************************************************#
            elif self.__class__.__name__ == "Roof_Cash_Battery_Cash_Page":
                if all([battery_tab, roof_tab, not rrr_tab, not solar_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Roof-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_BATTERY)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Roof-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Roof-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Roof-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Roof-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Roof-Cash and Battery-Cash Product,Kindly recheck")
    # tc_15*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Rrr_Cash_Page":
                if all([solar_tab, rrr_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and RRR-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and RRR-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Cash Product,Kindly recheck")
    # tc_16*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Roof_Sunnova_Battery_Cash_Page":
                if all([solar_tab, roof_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Roof-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and Roof-Sunnova and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Sunnova and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Sunnova and Battery-Cash , Kindly recheck")
    # tc_17*******************************************************************************************************#
            elif self.__class__.__name__ == "Rrr_Cash_Page":
                if all([rrr_tab, not solar_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof for RRR-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_ROOF)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified  for RRR-Cash Product , Continuing the Test")
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for RRR-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified  for RRR-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for RRR-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for RRR-Cash Product,Kindly recheck")
    # tc_18*******************************************************************************************************#
            elif self.__class__.__name__ == "Rrr_Service_Finance_Page":
                if all([rrr_tab, not solar_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof for RRR-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_ROOF)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for RRR-Service Finance, Continuing the Test")
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for RRR-Service Finance")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for RRR-Service Finance")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for RRR-Service Finance,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for RRR-Service Finance,Kindly recheck")
    # tc_19*******************************************************************************************************#
            elif self.__class__.__name__ == "Roof_Service_Finance_Page":
                if all([roof_tab, not solar_tab, not battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly,showing only Roof for Roof-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_ROOF)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Roof-Service Finance Product, Continuing the Test")
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Roof-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Roof-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Roof-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Roof only,for Roof-Service Finance Product,Kindly recheck")
    # tc_20*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Page":
                if all([solar_tab, not roof_tab, not battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly showing only Solar for Solar-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Solar only,for Solar-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Solar only,for Solar-Cash Product,Kindly recheck")
    # tc_21*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Roof_Sunnova_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Roof-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and Roof-Sunnova, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Sunnova")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Sunnova")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Sunnova,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Sunnova,Kindly recheck")
    # tc_22*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_RRR_Cash_Page":
                if all([solar_tab, rrr_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and RRR-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and RRR-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Cash Product,Kindly recheck")
    # tc_23*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Page":
                if all([solar_tab, not roof_tab, not battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly showing only Solar for Solar-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance Product , Continuing the Test")
                        self.sys_design_solar()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,System Design Tabs is not showing Solar only,for Solar-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,System Design Tabs is not showing Solar only,for Solar-Service Finance Product,Kindly recheck")
    # tc_24*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_service_finance_Rrr_service_finance_Page":
                if all([solar_tab, rrr_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and RRR-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and RRR-Service Finance Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Service Finance Product,Kindly recheck")
    # tc_25*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Roof_Cash_Battery_Cash":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Roof-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and Roof-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Cash and Battery-Cash Product,Kindly recheck")
    # tc_26*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_service_finance_Roof_service_finance_Page":
                if all([solar_tab, roof_tab, not battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Roof-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Roof-Service Finance Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Service Finance Product,Kindly recheck")
    # tc_27*******************************************************************************************************#
            elif self.__class__.__name__ == "Roof_Sunnova_Battery_Cash_Page":
                if all([roof_tab, battery_tab, not solar_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Roof-Sunnova and Battery-Cash Product")
                    self.invisibility_for_spinner()
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_BATTERY)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Roof-Sunnova and Battery-Cash Product, Continuing the Test")
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Roof-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Roof-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Roof-Sunnova and Battery-Cash Product,Kindly recheck ")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Roof-Sunnova and Battery-Cash Product,Kindly recheck")
    # tc_28*******************************************************************************************************#
            elif self.__class__.__name__ == "Roof_Service_Finance_Battery_Cash_Page":
                if all([roof_tab, battery_tab, not rrr_tab, not solar_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Roof-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_BATTERY)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Roof-Service Finance and Battery-Cash Product,Continuing the Test")
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Roof-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Roof-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Roof-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Roof-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_29*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Battery_Cash_Page":
                if all([solar_tab, battery_tab, not roof_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Battery-Cash Product,Kindly recheck")
    # tc_30*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Roof_Service_Finance_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Roof-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Roof-Service Finance Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Service Finance Product,Kindly recheck")
    # tc_31*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Battery_Cash_Page":
                if all([solar_tab, battery_tab, not rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_32*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Roof_service_finance_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Roof-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and Roof-Service Finance Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Service Finance Product,Kindly recheck")
    # tc_33*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Roof_Sunnova_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Roof-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Roof-Sunnova Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Sunnova Product,Kindly recheck")
    # tc_34*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Roof_Cash_Page":
                if all([solar_tab, roof_tab, not rrr_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Roof-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Roof-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Cash Product,Kindly recheck")
    # tc_35*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_RRR_Service_Finance_Page":
                if all([solar_tab, rrr_tab, not roof_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and RRR-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and RRR-Service Finance Product, Continuing the Test")
                        self.sys_design_solar()
                        time.sleep(1)
                        self.invisibility_for_spinner()
                        time.sleep(1)
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Service Finance Product,Kindly recheck")
    # tc_36*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_RRR_Sunnova_Page":
                if all([solar_tab, rrr_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and RRR-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and RRR-Sunnova Product, Continuing the Test")
                        self.sys_design_solar()
                        time.sleep(2)
                        self.invisibility_for_spinner()
                        time.sleep(1)
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Sunnova Product,Kindly recheck")
    # tc_37*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_RRR_service_finance_Page":
                if all([solar_tab, rrr_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and RRR-Service Finance Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and RRR-Service Finance Product, Continuing the Test")
                        self.sys_design_solar()
                        time.sleep(1)
                        self.invisibility_for_spinner()
                        time.sleep(1)
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Service Finance Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Service Finance Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Service Finance Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Service Finance Product,Kindly recheck")
    # tc_38*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_RRR_Sunnova_Page":
                if all([solar_tab, rrr_tab, not battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and RRR-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and RRR-Sunnova Product for Solar-Service Finance and RRR-Sunnova Product, Continuing the Test")
                        self.sys_design_solar()
                        time.sleep(1)
                        self.invisibility_for_spinner()
                        time.sleep(1)
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Sunnova Product,Kindly recheck")
    # tc_39*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_service_finance_Rrr_Cash_Page":
                if all([solar_tab, rrr_tab, not roof_tab, not battery_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and RRR-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and RRR-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Cash Product,Kindly recheck")
    # tc_40*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Roof_Service_Finance_Battery_Cash":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and Roof-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and Roof-Service Finance and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and Roof-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and Roof-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_41*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Roof_Service_Finance_Battery_Cash_Page":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Roof-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Roof-Service Finance and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Roof-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Roof-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_42*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Roof_Sunnova_Battery_Cash_Page":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Roof-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Roof-Sunnova and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Sunnova and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Sunnova and Battery-Cash Product,Kindly recheck")
    # tc_43*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Roof_Cash_Battery_Cash_Page":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Roof-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Roof-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Cash and Battery-Cash Product,Kindly recheck")
    # tc_44*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Roof_Service_Finance_Battery_Cash":
                if all([roof_tab, solar_tab, battery_tab, not rrr_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and Roof-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and Roof-Service Finance and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_roof()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and Roof-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and Roof-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_45*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_RRR_Sunnova_Battery_Cash_Page":
                if all([rrr_tab, solar_tab, battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova RRR-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova RRR-Sunnova and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova RRR-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova RRR-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly, Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly, Kindly recheck")
    # tc_46*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Rrr_Cash_Battery_Cash":
                if all([solar_tab, battery_tab, rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash RRR-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash RRR-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash RRR-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash RRR-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash RRR-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash RRR-Cash and Battery-Cash Product,Kindly recheck")
    # tc_47*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Rrr_Service_Finance_Battery_Cash":
                if all([solar_tab, battery_tab, rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and RRR-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and RRR-Service Finance and Battery-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_48*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_RRR_Service_Finance_Battery_Cash_Page":
                if all([rrr_tab, solar_tab, battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and RRR-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and RRR-Service Finance and Battery-Cash Product , Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and RRR-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and RRR-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_49*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Cash_Rrr_Sunnova_Battery_Cash_Page":
                if all([rrr_tab, solar_tab, battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Cash and RRR-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Cash and RRR-Sunnova and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Cash and RRR-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Sunnova and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Cash and RRR-Sunnova and Battery-Cash Product,Kindly recheck")
    # tc_50*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Rrr_Cash_Battery_Cash":
                if all([solar_tab, battery_tab, rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and RRR-Cash and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and RRR-Cash and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Cash and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Cash and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Cash and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Cash and Battery-Cash Product,Kindly recheck")
    # tc_51*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Rrr_Service_Finance_Battery_Cash":
                if all([solar_tab, battery_tab, rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and RRR-Service Finance and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and RRR-Service Finance and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Service Finance and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Service Finance and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Service Finance and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Service Finance and Battery-Cash Product,Kindly recheck")
    # tc_52*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Service_Finance_Rrr_Sunnova_Battery_Cash_Page":
                if all([rrr_tab, solar_tab, battery_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Service Finance and RRR-Sunnova and Battery-Cash Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Service Finance and RRR-Sunnova and Battery-Cash Product, Continuing the Test")
                        self.sys_design_solar()
                        self.sys_design_battery()
                        self.sys_design_rrr()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Sunnova and Battery-Cash Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Service Finance and RRR-Sunnova and Battery-Cash Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Sunnova and Battery-Cash Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Service Finance and RRR-Sunnova and Battery-Cash Product,Kindly recheck")
    # tc_53*******************************************************************************************************#
            elif self.__class__.__name__ == "Battery_Sunnova_Page":
                if all([battery_tab, not rrr_tab, not solar_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Battery-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_BATTERY)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Battery-Sunnova Product , Continuing the Test")
                        self.sys_design_battery()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Battery-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Battery-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Battery-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Battery-Sunnova Product,Kindly recheck")
    # tc_54*******************************************************************************************************#
            elif self.__class__.__name__ == "Solar_Sunnova_Battery_Sunnova_Page":
                if all([battery_tab, solar_tab, not rrr_tab, not roof_tab]):
                    log.logger.info(
                        "Product combination inside System Design is Populated Properly for Solar-Sunnova and Battery-Sunnova Product")
                    page_verify_util = self.is_displayed_xpath_el(
                        SDS.SYSTEM_DESIGN_PAGE_TITLE_SOLAR)
                    if page_verify_util:
                        log.logger.info(
                            "System Design page verified for Solar-Sunnova and Battery-Sunnova Product, Continuing the Test")
                        self.sys_design_battery()
                    else:
                        errors.append(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Battery-Sunnova Product")
                        log.logger.error(
                            "Test Failed!!,System Design page not verified for Solar-Sunnova and Battery-Sunnova Product")
                else:
                    errors.append(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Battery-Sunnova Product,Kindly recheck")
                    log.logger.error(
                        "Test Failed!!,Product combination inside System Design is not Populated Properly,for Solar-Sunnova and Battery-Sunnova Product,Kindly recheck")
    # ************************************************************************************************************#
            log.logger.info(
                "System Design Page Functionality Test Completed, Redirecting to Generate Quote Page..")
            self.button_click(OPS.NEXT)
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def automatic_sync_pop_up(self):
        try:
            sync_with_sunnova = self.is_displayed_xpath_el(
                GQS.SYNC_WITH_SUNNOVA_POPUP)
            if sync_with_sunnova:
                log.logger.info(
                    "Automatic Syncing in Progress, Checking any failure is there or not...")
                self.invisibility_for_spinner()
                time.sleep(2)
                failed = self.is_displayed_xpath_el(OPS.SUNNOVA_FAILED)
                pending = self.is_displayed_xpath_el(OPS.SUNNOVA_PENDING)
                if not failed or pending:
                    success = self.is_displayed_xpath_el(
                        OPS.SUNNOVA_SUCCESSFUL)
                    if success:
                        self.button_click(OPS.CLOSE_POPUP)
                    else:
                        errors.append(
                            "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                        log.logger.error(
                            "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                else:
                    errors.append(
                        "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
                    log.logger.error(
                        "Test Failed!!! Sunnova Syncing Failed, Please Recheck!!")
            else:
                log.logger.info(
                    "Automatic Syncing Not shown, Continuing the test..")
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def primary_contact_check(self):
        try:
            card = self.driver.find_elements(
                By.XPATH, OPS.CUSTOMER_INFORMATION_CARDS)
            lc = len(card)
            Primary_Uncheck = True

            for i in range(lc):
                self.driver.find_element(By.XPATH, OPS.card_len(i + 1)).click()
                time.sleep(2)
                primary_uncheck = self.is_displayed_xpath_el(
                    OPS.PRIMARY_CONTACT_UNCHECK)
                if primary_uncheck:
                    continue
                else:
                    log.logger.info(
                        f"Primary contact is selected for Contact {i + 1}")
                    Primary_Uncheck = False
            if Primary_Uncheck:
                errors.append(
                    "Primary contact is not selected for any contact,Test Failed!!")
                log.logger.error(
                    "Primary contact is not selected for any contact,Test Failed!!")
            time.sleep(2)
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def opportunity_page(self):
        try:
            time.sleep(1)
            log.logger.info(
                "Going to save the Opportunity Page after successful verifications and validations")
            self.invisibility_for_spinner()
            UTILITY_CHECK = self.is_displayed_xpath_el(OPS.UTILITY_CHECK)
            if not UTILITY_CHECK:
                self.button_click(OPS.UTILITY_UN_CHECK)
            self.primary_contact_check()
            time.sleep(1)
            log.logger.info(
                "Going to Save the Data")
            save_xpath = OPS.SAVE
            # Wait for the element to be clickable
            try:
                save_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, save_xpath))
                )
                # Click the element
                save_element.click()
                log.logger.info("Save button clicked successfully.")
            except TimeoutException:
                log.logger.error(
                    f"Timeout occurred while waiting for the Save button.")
                errors.append(
                    f"Timeout occurred while waiting for the Save button.")
            except Exception as e:
                log.logger.error(
                    f"An error occurred while clicking the Save button: {str(e)}")
                errors.append(
                    f"An error occurred while clicking the Save button: {str(e)}")
            time.sleep(2)
            popup_home_owner = self.is_displayed_xpath_el(OPS.POPUP)
            print("popup_home_owner", popup_home_owner)
            if popup_home_owner:
                try:
                    self.driver.execute_script(
                        f'document.querySelector("{OPS.CLOSE_HOME_POPUP_CSS}").click()')
                    log.logger.info(
                        "Close button for the home popup clicked successfully.")
                except NoSuchElementException:
                    errors.append(
                        f"Close button for the home popup not found.")
                except Exception as e:
                    errors.append(
                        f"An error occurred while clicking the close button for the home popup:{str(e)}")
                    log.logger.error(
                        f"An error occurred while clicking the close button for the home popup:{str(e)}")
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_of_alerts()
            time.sleep(1)
            self.invisibility_of_alerts()
            time.sleep(2)
            self.invisibility_of_alerts()
            self.wait_for_selector(OPS.NEXT_BTN_OP_PAGE)
            log.logger.info(
                "Saved the Opportunity, Clicking on Next Button..")
            next_xpath = OPS.NEXT_BTN_OP_PAGE
            try:
                next_element = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, next_xpath))
                )
                # Click the element
                next_element.click()
                log.logger.info("Next button clicked successfully.")
            except TimeoutException:
                log.logger.error(
                    "Timeout occurred while waiting for the Next button.")
                errors.append(
                    "Timeout occurred while waiting for the Next button.")
            except Exception as e:
                log.logger.error(
                    f"An error occurred while clicking the Next button: {str(e)}")
                errors.append(
                    f"An error occurred while clicking the Next button: {str(e)}")
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_of_alerts()
            time.sleep(1)
            log.logger.info(
                "Completed Opportunity Save and Proceeded to the Next Page")
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def sync_error_opportunity_page(self):
        try:
            time.sleep(1)
            err = self.is_displayed_xpath_el(OPS.SYNC_ERROR_NEXT_BUTTON)
            if err:
                log.logger.warning(
                    "Sync Error is populating for the Next Button Even the Opportunity is Synced and have Sunnova ID generated")
                ok_btn = self.driver.find_element(
                    OPS.SYNC_ERROR_NEXT_BUTTON_POPUP_OK)
                ok_btn.click()
                self.button_click(OPS.NEXT)
                log.logger.info(
                    "Completed Check Sync Error is populating for the Next Button Even the Opportunity is Synced and have Sunnova ID generated")
            else:
                pass
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def error_arr(self):
        return errors
