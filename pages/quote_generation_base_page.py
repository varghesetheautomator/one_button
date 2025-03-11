import logging
from selenium.webdriver.support.select import Select
from context.driver import driver
from selenium.webdriver.common.by import By
import time
from pages.base_page import Page
from utils.log_utils import Logger
from selector.opportunity_selectors import OpportunityPageSelectors as OPS
from selector.generate_quote_selectors import GenerateQuotePage as GQS
from selector.generate_contract_selectors import GenerateContractPage as GCS
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

errors = []
log = Logger(__name__, logging.INFO)


class QuotePage(Page):
    """Quote Page with Agreement Page Scripting for all Pages"""

    def __init__(self):
        super().__init__()
        self.driver = driver.get_driver()

    def get_sys_data_array_battery(self, value):
        self.sys_data_array_battery = None

    def get_sys_data_array_roof(self, value):
        self.sys_data_array_roof = None

    def solar_quote_creation_data_entry(self):
        try:
            # Finding the dropdown element for selecting finance method
            dropdown_element = self.driver.find_element(
                By.XPATH, GQS.FINANCE_METHOD)
            select = Select(dropdown_element)
            options = [option.text for option in select.options]

            # Checking if PPA-EZ option is present
            ppa_ez_option_present = any(
                option.text == "PPA-EZ" for option in select.options)
            if ppa_ez_option_present:
                # Selecting PPA-EZ if it's present
                select.select_by_visible_text("PPA-EZ")
                log.logger.info("Selected Finance Method as PPA-EZ ")
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)

                # Selecting Pricing Method as Rate
                pricing_method = Select(
                    self.driver.find_element(By.XPATH, GQS.PRICING_METHOD))
                time.sleep(2)
                pricing_method.select_by_visible_text("Rate")
                self.invisibility_for_spinner()
                log.logger.info("Selected Pricing Method as Rate ")

                # Entering Pricing Value
                pricing_value = self.driver.find_element(
                    By.XPATH, GQS.PRICING_VALUE)
                pricing_value.click()
                pricing_value.clear()
                pricing_value.send_keys("0.036")
                log.logger.info("Entered Pricing Value as 0.036")
                self.invisibility_for_spinner()
            else:
                # If PPA-EZ option is not present
                log.logger.info(
                    "PPA-EZ Option is not present for this Opportunity")

                # Checking if Lease option is present
                lease_option_present = any(
                    option.text == "Lease" for option in select.options)
                if lease_option_present:
                    # Selecting Lease if it's present
                    select.select_by_visible_text("Lease")
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(2)
                    log.logger.info("Selected Finance Method as Lease")

                    # Selecting Pricing Method as PPW
                    pricing_method = self.driver.find_element(
                        By.XPATH, GQS.PRICING_METHOD)
                    select = Select(pricing_method)
                    select.select_by_visible_text("PPW")
                    self.invisibility_for_spinner()

                    # Entering Pricing Value
                    pricing_value = self.driver.find_element(
                        By.XPATH, GQS.PRICING_VALUE)
                    pricing_method.click()
                    pricing_value.clear()
                    pricing_value.send_keys("2.69")
                    log.logger.info("Entered Pricing Value as 2.69")
                    self.invisibility_for_spinner()
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    self.invisibility_for_spinner()
                else:
                    # If neither PPA-EZ nor Lease options are present, select Loan
                    select.select_by_visible_text("Loan")
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(2)
                    log.logger.info("Selected Finance Method as Loan")

                    # Entering Desired PPW Net
                    desired_ppw = self.driver.find_element(
                        By.XPATH, GQS.DESIRED_PPW)
                    desired_ppw.click()
                    desired_ppw.clear()
                    desired_ppw.send_keys("5")
                    log.logger.info("Entered Desired PPW Net as 5")
                    self.invisibility_for_spinner()
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    self.invisibility_for_spinner()
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def roof_quote_creation_data_entry(self):
        try:
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(3)
            self.wait_for_selector(GQS.ROOF_FINANCE_METHOD_DROPDOWN)
            # print("system_design_data_roof", self.sys_data_array_roof[0])
            finance_method = Select(self.driver.find_element(
                By.XPATH, GQS.ROOF_FINANCE_METHOD_DROPDOWN))
            finance_method_default = finance_method.first_selected_option.text
            # print("finance_method_default", finance_method_default)
            if finance_method_default == "Cash Contract":
                log.logger.info("The Finance Method Selected is Cash Contract")
                roof_quote_data = []
                scroll = "document.querySelector('button[id=\"generate-quote-button\"]').scrollIntoView()"
                self.driver.execute_script(scroll)
                time.sleep(2)
                roof_manufacturer = self.driver.find_element(
                    By.XPATH, GQS.SHINGLE_MANUFACTURER).text
                roof_prod = self.driver.find_element(
                    By.XPATH, GQS.SHINGLE_PRODUCT).text
                roof_sq = self.driver.find_element(
                    By.XPATH, GQS.ROOF_SQUARE_OVERRIDE_QUOTE).text
                # print("self.sys_data_array_roof[0]",
                #       self.sys_data_array_roof[0])
                roof_quote_data.append([roof_manufacturer, roof_prod, roof_sq])
                # print("quote_data_roof", roof_quote_data[0])
                if roof_quote_data[0] == self.sys_data_array_roof[0]:
                    log.logger.info(f"Roof values matches in the quote page")
                else:
                    log.logger.error(
                        f"Roof values do not match in the quote page")
                    errors.append(
                        f"Roof values do not match in the quote page")
            else:
                roof_fin_dropdown = self.driver.find_element(
                    By.XPATH, GQS.ROOF_QUOTE_FIN_METHOD)
                select = Select(roof_fin_dropdown)
                # Check if "Accessory_Loan" is present
                time.sleep(3)
                options = [option.text for option in select.options]
                accessory_loan_option = any(
                    option.text == "Accessory_Loan" for option in select.options)
                # print(options)
                if accessory_loan_option:
                    time.sleep(1)
                    select.select_by_visible_text("Accessory_Loan")
                    time.sleep(1)
                    log.logger.info(
                        "Selected Finance Method as Accessory Loan for Roof")
                else:
                    cash_contract_option = any(
                        option.text == "Cash Contract" for option in select.options)
                    if cash_contract_option:
                        time.sleep(1)
                        select.select_by_value("Cash Contract")
                        time.sleep(1)
                        log.logger.info(
                            "Selected Finance Method as Cash Contract for Roof")
                    else:
                        select.select_by_value("Loan")
                        time.sleep(1)
                        log.logger.info(
                            "Selected Finance Method as Loan Contract for Roof")
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors

    def battery_quote_creation_data_entry(self):
        try:
            time.sleep(2)
            # Printing system design data for debugging purposes
            # print("system_design_data_battery", self.sys_data_array_battery[0])
            # Initializing a list to store battery quote data
            battery_quote_data = []
            # Extracting battery name and count from the quote page
            battery_name = self.driver.find_element(
                By.XPATH, GQS.QUOTE_BATTERY_NAME).text
            count = self.driver.find_element(
                By.XPATH, GQS.QUOTE_BATTERY_COUNT).text

            # Appending battery quote data to the list
            battery_quote_data.append([battery_name, count])
            # print("quote_data_battery", battery_quote_data[0])

            # Checking if battery quote data matches system design data
            if battery_quote_data[0] == self.sys_data_array_battery[0]:
                log.logger.info(f"Battery value matches in the quote page")
            else:
                log.logger.error(
                    f"Battery value do not match in the quote page")
                errors.append(f"Battery value do not match in the quote page")

            # Checking battery cost subtotal
            battery_cost_subtotal = self.driver.find_element(
                By.XPATH, GQS.BATTERY_COST_SUBTOTAL).text
            if battery_cost_subtotal is not None:
                log.logger.info(
                    "Battery Subtotal Cost value is not Null, Continuing the Test")
            else:
                # If battery cost subtotal is null, log error and append to errors list
                errors.append(
                    "Test Failed!!, Battery Subtotal Cost value is Null")
                log.logger.error(
                    "Test Failed!!, Battery Subtotal Cost value is Null")
            battery_adder = self.is_displayed_xpath_el(
                GQS.CHOOSE_BATTERY_ADDER_HEADER)
            if battery_adder:
                self.driver.execute_script(
                    f'document.querySelector("{GQS.BATTERY_FIRE_ENCLOSURE_CSS}").click()')
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                self.driver.execute_script(
                    f'document.querySelector("{GQS.LUMIN_SMART_PANEL_CSS}").click()')
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)
                self.driver.find_element(
                    By.XPATH, GQS.BATTERY_ADDER_COST_SUBTOTAL).click()
                battery_add_cost = self.driver.find_element(
                    By.XPATH, GQS.BATTERY_ADDITIONAL_COST)
                battery_add_cost.clear()
                battery_add_cost.send_keys("100")
                self.invisibility_for_spinner()
                time.sleep(1)
                self.driver.find_element(
                    By.XPATH, GQS.BATTERY_ADDER_COST_SUBTOTAL).click()
                self.invisibility_for_spinner()
                time.sleep(1)
                battery_add_cost_subtotal = self.driver.find_element(
                    By.XPATH, GQS.BATTERY_ADDER_COST_SUBTOTAL).text
                # print(battery_add_cost_subtotal)
                battery_add_cost_est_sub_total = "$4,100.00"

                if battery_add_cost_subtotal == battery_add_cost_est_sub_total:
                    log.logger.info(
                        f"Battery Subtotal Validated successfully, Actual figure : {battery_add_cost_subtotal} is getting tallied with the estimated figure : {battery_add_cost_est_sub_total}")
                else:
                    errors.append(
                        f"Test Failed!!, Battery Subtotal Validation Failed, Actual figure : {battery_add_cost_subtotal} is not tallied with the estimated figure : {battery_add_cost_est_sub_total}")
                    log.logger.error(
                        f"Test Failed!!, Battery Subtotal Validation Failed, Actual figure : {battery_add_cost_subtotal} is not tallied with the estimated figure : {battery_add_cost_est_sub_total}")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        # Returning the errors list
        return errors

    def agreement_page_popup(self):
        try:
            # Checking if the popup is displayed
            self.wait_for_selector(OPS.POPUP)
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                # If popup is displayed, click on cancel button
                self.driver.find_element(By.XPATH, GCS.POPUP_CANCEL).click()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                # Checking if contract page is displayed after closing popup
                contract_page = self.is_displayed_xpath_el(GCS.CONTRACT_PAGE)
                if contract_page:
                    # If contract page is displayed, verify its main title names
                    contract_page_text = self.driver.find_element(
                        By.XPATH, GCS.CONTRACT_PAGE).text
                    log.logger.info(
                        f"Contract Page Verified with the Main Title Names as : {contract_page_text}")
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    self.invisibility_for_contract_wait_spinner()
                    # Checking for sync error on contract page
                    sync_error = self.is_displayed_xpath_el(
                        GCS.CONTRACT_PAGE_SYNC_ERROR)
                    if sync_error:
                        # If sync error is displayed, close it
                        close = self.is_displayed_xpath_el(GCS.CLOSE_ERROR)
                        if close:
                            close = self.driver.find_element(
                                By.XPATH, GCS.CLOSE_ERROR)
                            close.click()
                            time.sleep(2)
                    else:
                        pass
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def click_generate_quote_button(self):
        try:
            # Scroll to the generate quote button
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, GQS.GENERATE_QUOTE_CSS))
            )

            excel_icon = self.driver.find_element(
                By.XPATH, GQS.EXCEL_ICON)
            excel_icon.click()
            time.sleep(1)
            close = self.is_displayed_xpath_el(GQS.CLOSE_EXCEl_POPUP)
            if close:
                self.driver.find_element(
                    By.XPATH, GQS.CLOSE_EXCEl_POPUP).click()
                self.invisibility_for_spinner()
                time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.driver.execute_script(
                f'document.querySelector("{GQS.GENERATE_QUOTE_CSS}").scrollIntoView()')
            # Click the generate quote button
            self.driver.execute_script(
                f'document.querySelector("{GQS.GENERATE_QUOTE_CSS}").click()')
            # Wait for spinner to disappear
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            # Wait for potential automatic sync pop-up
            self.automatic_sync_pop_up()
            # Verify if all quote version tabs are displayed
            quote_version_tabs_verification = self.is_displayed_xpath_el(
                GQS.ALL_QUOTES_RADIO_BTN)
            if not quote_version_tabs_verification:
                # If quote version tabs are not displayed, click generate quote button again
                self.driver.execute_script(
                    f'document.querySelector("{GQS.GENERATE_QUOTE_CSS}").scrollIntoView()')
                log.logger.info(
                    "Generate Quote Click Not Worked Well as expected, clicking it again")
                self.driver.execute_script(
                    f'document.querySelector("{GQS.GENERATE_QUOTE_CSS}").click()')
                time.sleep(1)
                # Wait for spinner to disappear
                self.invisibility_for_spinner()
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(1)
                # Wait for potential automatic sync pop-up
                self.automatic_sync_pop_up()
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}", exc_info=True)

        # Returning the errors list
        return errors

    def view_trinity_proposal(self, id):
        try:
            # Logging info about proceeding to click View Trinity Proposal
            log.logger.info(f"Going to click View Trinity Proposal")
            self.invisibility_for_spinner()
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            # Closing any sync error popups if present
            self.sync_error_close()
            time.sleep(1)
            # Finding and clicking the View Trinity Proposal button
            self.wait_for_selector(GCS.view_trinity_proposal(id))
            view_finance_partner_proposal = self.driver.find_element(
                By.XPATH, GCS.view_trinity_proposal(id))
            view_finance_partner_proposal.click()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(2)
            # Checking if the popup is displayed
            self.wait_for_selector(OPS.POPUP)
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                self.wait_for_selector(GCS.VIEW_TRINITY_PROPOSAL_BUTTON)
                link = self.is_displayed_xpath_el(
                    GCS.VIEW_TRINITY_PROPOSAL_BUTTON)
                if link:
                    # Clicking on the document link
                    links = self.driver.find_element(
                        By.XPATH, GCS.VIEW_TRINITY_PROPOSAL_BUTTON)
                    links.click()
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    # Checking if the PDF link is visible
                    pdf_link = self.is_displayed_xpath_el(
                        GCS.VIEW_TRINITY_PROPOSAL_PDF_LINK)
                    if pdf_link:
                        # Clicking on the PDF link and handling it
                        self.driver.find_element(
                            By.XPATH, GCS.VIEW_TRINITY_PROPOSAL_PDF_LINK).click()
                        time.sleep(3)
                        self.driver.switch_to.window(
                            self.driver.window_handles[0])
                        time.sleep(1)
                        close = self.driver.find_element(
                            By.XPATH, GCS.CLOSE_BTN)
                        close.click()
                        time.sleep(1)
                        log.logger.info(
                            f"Completed Clicking View Trinity Proposal")
                    else:
                        errors.append(
                            "Test Failed!!Combined Pack PDF Link Failed to Generate for View Trinity Contract")
                        log.logger.error(
                            "Test Failed!!Combined Pack PDF Link Failed to Generate for View Trinity Contract")
                else:
                    errors.append(
                        "Test Failed!!Document Link Failed to Generate for View Trinity Document Link")
                    log.logger.error(
                        "Test Failed!!Document Link Failed to Generate for View Trinity Document Link")
            else:
                log.logger.error("View Trinity Proposal Pop up is not Visible")
                errors.append("View Trinity Proposal Pop up is not Visible")
            time.sleep(2)
            log.logger.info(f"Completed View Trinity Proposal")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def view_finance_partner_proposal(self, id):
        try:
            # Waiting for contract wait spinner to disappear
            self.invisibility_for_contract_wait_spinner()
            self.invisibility_for_spinner()
            self.invisibility_for_contract_wait_spinner()
            self.invisibility_for_spinner()
            log.logger.info(f"Going to click View Finance Partner Proposal")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            # Closing any sync error popups if present
            self.sync_error_close()
            time.sleep(2)
            self.wait_for_selector(GCS.view_finance_partner_agreement(id))
            # Finding and clicking the View Finance Partner Proposal button
            view_finance_partner_proposal = self.driver.find_element(
                By.XPATH, GCS.view_finance_partner_agreement(id))
            view_finance_partner_proposal.click()
            # Waiting for spinner to disappear
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            # Checking if the popup is displayed
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                # Getting the message displayed in the popup
                message_visible = self.is_displayed_xpath_el(
                    GCS.VIEW_PROPOSAL_SOLAR_MESSAGE)
                if message_visible:
                    message = self.driver.find_element(
                        By.XPATH, GCS.VIEW_PROPOSAL_SOLAR_MESSAGE).text
                    log.logger.info(
                        f"Message showing in View Proposal Popup is {message}")
                    # Checking if the file link is visible for download
                    file = self.is_displayed_xpath_el(
                        GCS.VIEW_PROPOSAL_SOLAR_FILE_CLICK_HERE)
                    if file:
                        # If file link is visible, clicking on the Download Button
                        log.logger.info(
                            "File is Visible for Download, Clicking on Download Button")
                        generate_file = self.driver.find_element(
                            By.XPATH, GCS.VIEW_PROPOSAL_SOLAR_FILE_CLICK_HERE)
                        generate_file.click()
                        time.sleep(3)
                        self.driver.switch_to.window(
                            self.driver.window_handles[0])
                        time.sleep(2)
                    else:
                        # If file link is not visible, logging a warning
                        log.logger.warning(
                            "Test Failed!!! File is Not Visible for Download, Clicking on Download Button, Please Recheck!!")
                else:
                    # If file Message is not visible, logging a warning
                    log.logger.warning(
                        "Test Failed!!! The Message is Not Visible in the Popup, Please Recheck!!")

                # Closing the popup
                self.driver.find_element(By.XPATH, GCS.CLOSE_BTN).click()
                time.sleep(2)
                self.sync_error_close()
            else:
                # If popup is not visible, logging an error
                self.sync_error_close()
                log.logger.warning("View Proposal Solar Pop up is not Visible")
                # errors.append("View Proposal Solar Pop up is not Visible")

            # Waiting for 2 seconds
            time.sleep(2)
            log.logger.info(f"Completed View Finance Partner Proposal")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def sign_finance_partner_proposal(self, id):
        try:
            # Logging info about proceeding to click Sign Finance Partner Contract
            log.logger.info(f"Going to click Sign Finance Partner Contract")
            self.invisibility_for_spinner()
            time.sleep(1)
            # Scrolling to the top of the page
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            self.sync_error_close()
            # Checking if the contract is generated
            contract_generated = self.is_displayed_xpath_el(
                GCS.sign_finance_partner_contract(id))
            # Closing any sync error popups if present
            self.sync_error_close()
            if contract_generated:
                # If contract is generated, clicking on the contract icon
                sign_finance_partner_proposal = self.driver.find_element(By.XPATH,
                                                                         GCS.sign_finance_partner_contract(id))
                sign_finance_partner_proposal.click()
                time.sleep(1)

                # Checking if the popup is displayed
                popup = self.is_displayed_xpath_el(OPS.POPUP)

                if popup:
                    # If popup is displayed, clicking on the generate contract button
                    generate_contract = self.driver.find_element(
                        By.XPATH, GCS.GENERATE_SUNNOVA_CONTRACT_BTN)
                    generate_contract.click()
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    # Checking if there's an error message displayed
                    err = self.is_displayed_xpath_el(
                        GCS.SIGN_FINANCE_PARTNER_CONTRACT_ERROR)
                    if err:
                        # If error message is displayed, logging a warning
                        msg = self.driver.find_element(
                            By.XPATH, GCS.SIGN_FINANCE_PARTNER_CONTRACT_ERROR).text
                        log.logger.warning(
                            f"Warning, Error Message is showing with the text as : {msg}")
                    else:
                        pass  # Yet to Code for the passed Credit

                    # Closing the contract popup
                    self.driver.find_element(
                        By.XPATH, GCS.CLOSE_FINANCE_PARTNER_CONTRACT_POP_UP).click()
                    time.sleep(2)
                    self.sync_error_close()
                else:
                    time.sleep(4)
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(2)
            else:
                # If contract icon is not visible, appending an error message
                errors.append(
                    "Sign finance partner proposal eye icon not visible")
                log.logger.error(
                    "Sign finance partner proposal eye icon not visible")

            # Logging info that Sign Finance Partner Contract process is completed
            log.logger.info(f"Completed Sign Finance Partner Contract")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def sfdc_sync(self, id):
        try:
            # Logging info about proceeding to click SFDC Sync
            log.logger.info(f"Going to click SFDC Sync")
            self.driver.execute_script("window.scrollTo(0, 0);")
            # Waiting for spinner to disappear
            self.invisibility_for_spinner()
            time.sleep(1)
            # Closing any sync error popups if present
            self.sync_error_close()
            self.wait_for_selector(GCS.sfdc_sync(id))

            # Finding and clicking the SFDC Sync button
            sfdc = self.driver.find_element(By.XPATH, GCS.sfdc_sync(id))
            sfdc.click()
            time.sleep(1)

            # Waiting for spinner to disappear
            self.invisibility_for_spinner()
            time.sleep(3)
            self.invisibility_for_spinner()
            time.sleep(1)
            # Checking if the popup is displayed
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                # If popup is displayed, checking if SFDC Syncing failed
                failed = self.is_displayed_xpath_el(OPS.SUNNOVA_FAILED)
                if failed:
                    log.logger.warning(
                        "Warning!!! SFDC Syncing Failed, Please Recheck!!")
                else:
                    log.logger.info("SFDC Sync Successfully Completed")

                # Closing the SFDC Sync popup
                self.driver.find_element(By.XPATH, GCS.CLOSE_SFDC).click()
                time.sleep(1)
                # Checking if there's a sync error on contract page
                self.sync_error_close()
                log.logger.info(f"Completed SFDC Sync")
            else:
                # If SFDC Sync popup is not visible, appending an error message
                log.logger.error(
                    "Test Failed !! SFDC Sync Pop up is not visible")
                errors.append("Test Failed !! SFDC Sync Pop up is not visible")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def view_combined_pack(self, id):
        try:
            # Logging info about proceeding to click View Combined Pack
            log.logger.info(f"Going to click View Combined Pack")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            # Closing any sync error popups if present
            self.sync_error_close()
            # Checking if there's a sync error on contract page
            sync_error = self.is_displayed_xpath_el(
                GCS.CONTRACT_PAGE_SYNC_ERROR)
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(2)
            self.wait_for_selector(GCS.view_combined_pack(id))
            # Finding and clicking the View Combined Pack button
            view_combined_pack = self.driver.find_element(
                By.XPATH, GCS.view_combined_pack(id))
            view_combined_pack.click()
            time.sleep(1)
            # Waiting for spinner to disappear
            self.invisibility_for_spinner()
            time.sleep(3)
            self.wait_for_selector(OPS.POPUP)
            # Checking if the popup is displayed
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                # Checking if the link to view the combined pack is visible
                link = self.is_displayed_xpath_el(
                    GCS.VIEW_TRINITY_CONTRACT_LINK)
                if link:
                    # If link is visible, clicking on it
                    links = self.driver.find_element(
                        By.XPATH, GCS.VIEW_TRINITY_CONTRACT_LINK)
                    links.click()
                    time.sleep(4)
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(2)
                else:
                    # If link is not visible, logging a warning
                    errors.append(
                        "Test Failed!! Document Link Failed to Generate for View Trinity Document Link in combined pack")
                    log.logger.error(
                        "Test Failed!! Document Link Failed to Generate for View Trinity Document Link in combined pack")
            else:
                # If popup is not visible, appending an error message
                errors.append(
                    "Test Failed!! View Trinity Document Popup Not Visible")
                log.logger.error(
                    "Test Failed!! View Trinity Document Popup Not Visible")

            # Closing the popup
            close = self.driver.find_element(By.XPATH, GCS.CLOSE_BTN)
            close.click()
            self.sync_error_close()
            # Logging info that View Combined Pack process is completed
            log.logger.info(f"Completed Clicking View Combined Pack")

            # Waiting for 1 second
            time.sleep(1)
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def sign_combined_pack(self, id):
        try:
            # Logging info about proceeding to click Sign Combined Pack
            log.logger.info("Going to click Sign Combined Pack")
            self.driver.execute_script("window.scrollTo(0, 0);")
            # Waiting for contract wait spinner to disappear
            self.wait_for_selector(GCS.sign_combined_pack(id))
            self.sync_error_close()
            # Finding and clicking the Sign Combined Pack button
            view_trinity_contract = self.driver.find_element(
                By.XPATH, GCS.sign_combined_pack(id))
            view_trinity_contract.click()
            time.sleep(1)

            # Waiting for spinner to disappear
            self.invisibility_for_spinner()
            time.sleep(1)

            # Checking if the popup is displayed
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                # Checking if the checkbox to sign the contract is visible
                cb = self.is_displayed_xpath_el(
                    GCS.CHECK_BOX_SIGN_TRINITY_CONTRACT)
                if cb:
                    # If checkbox is visible, clicking on it
                    self.driver.find_element(
                        By.XPATH, GCS.CHECK_BOX_SIGN_TRINITY_CONTRACT).click()

                    # Selecting contact mail option
                    contact = Select(self.driver.find_element(
                        By.XPATH, GCS.CONTACT_MAIL_SIGN_TRINITY_CONTRACT))
                    time.sleep(2)
                    contact.select_by_visible_text("InPerson")
                    time.sleep(1)

                    # Clicking on the generate contract button
                    self.button_click(GCS.GENERATE_CONTRACT_BTN)

                    # Checking if there's an error while generating the contract
                    error = self.is_displayed_xpath_el(
                        GCS.SIGN_TRINITY_CONTRACT_FILE_ERROR)
                    if error:
                        log.logger.warning(
                            "Test Failed!! Error Showing, File Link Not Generating due to error")
                    else:
                        # Checking if e-sign link is visible
                        e_sign = self.is_displayed_xpath_el(GCS.E_SIGN_LINK)
                        if e_sign:
                            # If e-sign link is visible, clicking on it
                            self.button_click(GCS.E_SIGN_LINK)
                            time.sleep(3)
                            self.driver.switch_to.window(
                                self.driver.window_handles[0])
                            time.sleep(1)
                            close = self.driver.find_element(
                                By.XPATH, GCS.CLOSE_BTN)
                            close.click()
                        else:
                            log.logger.warning(
                                "e Sign Link Not Showing for this Opportunity for Review and Sign")

                    # Logging completion of sign combined pack process
                    log.logger.info("Completed Sign Combined Pack")
                else:
                    # If checkbox is not visible, appending an error message
                    errors.append(
                        "Test Failed!! Checkbox is not Visible for Sign Trinity Contract")
                    log.logger.error(
                        "Test Failed!! Checkbox is not Visible for Sign Trinity Contract")
            else:
                # If popup is not visible, appending an error message
                errors.append(
                    "Test Failed!! Sign Trinity Document Popup Not Visible")
                log.logger.error(
                    "Test Failed!! Sign Trinity Document Popup Not Visible")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def view_roof_proposal(self, id):
        try:
            # Logging info about proceeding to click View Roof Proposal
            log.logger.info(f"Going to click View Roof Proposal")
            self.driver.execute_script("window.scrollTo(0, 0);")
            # Closing any sync error popups if present
            self.sync_error_close()
            time.sleep(1)
            # Scrolling to the top of the page
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.wait_for_selector(GCS.view_roof_proposal(id))
            # Finding and clicking the View Roof Proposal button
            roof_proposal = self.driver.find_element(
                By.XPATH, GCS.view_roof_proposal(id))
            roof_proposal.click()
            time.sleep(1)
            # Waiting for spinner to disappear
            self.invisibility_for_spinner()
            time.sleep(1)
            self.sync_error_close()
            # Checking if the popup is displayed
            popup = self.is_displayed_xpath_el(OPS.POPUP)
            if popup:
                # Checking if the link to view the proposal is visible
                link = self.is_displayed_xpath_el(
                    GCS.VIEW_TRINITY_PROPOSAL_BUTTON)
                if link:
                    # If link is visible, clicking on it
                    links = self.driver.find_element(
                        By.XPATH, GCS.VIEW_TRINITY_PROPOSAL_BUTTON)
                    links.click()
                    time.sleep(1)
                    self.invisibility_for_spinner()
                    time.sleep(1)

                    # Checking if the PDF link is visible
                    pdf_link = self.is_displayed_xpath_el(
                        GCS.VIEW_TRINITY_PROPOSAL_PDF_LINK)
                    if pdf_link:
                        # If PDF link is visible, clicking on it
                        self.driver.find_element(
                            By.XPATH, GCS.VIEW_TRINITY_PROPOSAL_PDF_LINK).click()
                        time.sleep(3)
                        self.driver.switch_to.window(
                            self.driver.window_handles[0])
                        time.sleep(1)
                        close = self.driver.find_element(
                            By.XPATH, GCS.CLOSE_BTN)
                        close.click()
                        time.sleep(1)
                        self.sync_error_close()
                        log.logger.info(
                            f"Completed Clicking View Roof Proposal")
                    else:
                        errors.append(
                            "Test Failed!! Combined Pack PDF Link Failed to Generate for View Trinity Contract")
                        log.logger.error(
                            "Test Failed!! Combined Pack PDF Link Failed to Generate for View Trinity Contract")
                else:
                    errors.append(
                        "Test Failed!! Document Link Failed to Generate for View Trinity Document Link")
                    log.logger.error(
                        "Test Failed!! Document Link Failed to Generate for View Trinity Document Link")
            else:
                errors.append(
                    "Test Failed!! View Trinity Document Popup Not Visible")
                log.logger.error(
                    "Test Failed!! View Trinity Document Popup Not Visible")
        except Exception as e:
            # Handling exceptions and appending error details to errors list
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")

        # Returning the errors list
        return errors

    def generate_quote_and_agreement_validations(self):
        try:
            # Checking if the quote summary popup is displayed and canceling it if shown
            quote_summary_data_pop_up = self.is_displayed_xpath_el(
                GQS.QUOTE_SUMMARY_POPUP)
            if quote_summary_data_pop_up:
                log.logger.info(
                    "Generate Quote Summary Popup Shown for Automatic Quote Creation as per the details from Sales Rep, Cancelling the Quote Creation")
                self.button_click(GQS.CANCEL_QUOTE_SUMMARY_POPUP)
            else:
                pass
            # Checking for errors in the automatic sync popup
            error_count = self.automatic_sync_pop_up()
            if len(error_count) > 0:
                log.logger.error(
                    f"Automatic Sync Popup has {error_count} error(s). Skipping the execution of the subsequent code.")
                errors.append(
                    f"Automatic Sync Popup has {error_count} error(s). Skipping the execution of the subsequent code.")
            # Waiting for spinners to disappear
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(1)
            self.invisibility_for_spinner()
            time.sleep(2)
            # Checking for errors in the automatic sync popup again
            error_count = self.automatic_sync_pop_up()
            if len(error_count) > 0:
                log.logger.error(
                    f"Automatic Sync Popup has {error_count} error(s). Skipping the execution of the subsequent code.")
                errors.append(
                    f"Automatic Sync Popup has {error_count} error(s). Skipping the execution of the subsequent code.")

            # Checking for different quote titles and performing actions accordingly
            solar_quote_title = self.is_displayed_xpath_el(
                GQS.SOLAR_QUOTE_TITLE)
            battery_quote_title = self.is_displayed_xpath_el(
                GQS.BATTERY_QUOTE_TITLE)
            roof_quote_title = self.is_displayed_xpath_el(GQS.ROOF_QUOTE_TITLE)
            rrr_quote_title = self.is_displayed_xpath_el(GQS.RRR_QUOTE_TITLE)

            if solar_quote_title:
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)
                finance_partner = self.driver.find_element(
                    By.XPATH, GQS.FINANCE_PARTNER)
                select = Select(finance_partner)
                selected_option = select.first_selected_option.text
                time.sleep(1)
                # print(selected_option)
                if selected_option == "Cash":
                    log.logger.info(
                        f"Finance Partner for the Opportunity is {selected_option}")
                    desired_ppw = self.driver.find_element(
                        By.XPATH, GQS.DESIRED_PPW)
                    desired_ppw.click()
                    desired_ppw.clear()
                    desired_ppw.send_keys("2.69")
                    time.sleep(1)
                    self.invisibility_for_spinner()
                else:
                    self.solar_quote_creation_data_entry()
                    self.invisibility_for_spinner()
                    time.sleep(1)
                    self.invisibility_for_spinner()
            if battery_quote_title:
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)
                self.battery_quote_creation_data_entry()
            if roof_quote_title:
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)
                self.roof_quote_creation_data_entry()
            if rrr_quote_title:
                time.sleep(1)
                self.invisibility_for_spinner()
                time.sleep(2)
                self.roof_quote_creation_data_entry()
            self.invisibility_for_spinner()
            time.sleep(1)
            # Clicking the generate quote button
            self.click_generate_quote_button()
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")
# TC-01***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Page":
                log.logger.info("Entering to Solar Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar Product")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                system_id_solar = self.driver.find_element(
                    By.XPATH, GQS.system_id_following_quote(max_index + 1)).text
                if system_id_solar != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar}")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # print("System ID Generated for Solar Sunnova Product", system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar-Sunnova Product...")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID is not generated for this Quote, and is generated as {system_id_solar}")
                    errors.append(
                        f"Test Failed!!, System ID is not generated for this Quote, and is generated as {system_id_solar}")
# TC-02***********************************************************************************************************************#
            if self.__class__.__name__ == "Roof_Sunnova_Page":
                log.logger.info("Entering to Roof Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Roof Product")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.system_id_following_quote(max_index + 1)).text
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.system_id_following_quote(max_index)).text
                if system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof}")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(system_id_value)
                    # print("System ID Generated for Roof Sunnova Product",
                    #       system_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Roof-Sunnova Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_roof)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_roof)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_roof)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_roof)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        view_roof_proposal_err = self.view_roof_proposal(
                                            system_id_roof)
                                        if len(view_roof_proposal_err) > 0:
                                            break
                    # self.view_finance_partner_proposal(system_id_roof)
                    # self.sign_finance_partner_proposal(system_id_roof)
                    # self.sfdc_sync(system_id_roof)
                    # self.view_combined_pack(system_id_roof)
                    # self.view_roof_proposal(system_id_roof)
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID is not generated for this Quote, and is generated as {system_id_roof}")
                    errors.append(
                        f"Test Failed!!, System ID is not generated for this Quote, and is generated as {system_id_roof}")
# TC-03***********************************************************************************************************************#
            if self.__class__.__name__ == "Roof_Cash_Page":
                log.logger.info("Entering to Roof Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID number for Roof Product")
                quote_array_roof_cash = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_TEXT)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_array_roof_cash.append(number)
                max_index = quote_array_roof_cash.index(
                    max(quote_array_roof_cash))
                quote_id_value = max(quote_array_roof_cash)
                # print("Array in Quote Page is ", quote_array)
                if quote_id_value is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_value} for Roof Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    quote_ID = self.driver.find_elements(
                        By.XPATH, GCS.QUOTE_IDS)
                    quote_ID_arr_roof = []
                    for i in range(len(quote_ID)):
                        quote_ids_text = self.driver.find_element(
                            By.XPATH, GCS.quote_ids(i + 1)).text
                        q_number = quote_ids_text.split()[-1]
                        quote_ID_arr_roof.append(q_number)
                    quote_ID_contract_page = max(quote_ID_arr_roof)
                    if quote_id_value == quote_ID_contract_page:
                        log.logger.info(
                            f"Validation completed for Quote Number with generated quote number as {quote_ID_contract_page} for Roof Product ")
                        log.logger.info(
                            "Validating Contract Page Documents for Roof-Cash Product")
                        for i in range(1):
                            view_trinity_proposal_err = self.view_trinity_proposal(
                                quote_ID_contract_page)
                            if len(view_trinity_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(
                                    quote_ID_contract_page)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        quote_ID_contract_page)
                                    if len(view_combined_pack_err) > 0:
                                        break

                        # self.view_trinity_proposal(quote_ID_contract_page)
                        # self.sfdc_sync(quote_ID_contract_page)
                        # self.view_combined_pack(quote_ID_contract_page)

                    else:
                        log.logger.error(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for Roof "
                            f"Product")
                        errors.append(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for Roof "
                            f"Product")

                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated as {quote_id_value}")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote for Roof Product, and is generated as {quote_id_value}")
# TC-04***********************************************************************************************************************#
            if self.__class__.__name__ == "Battery_Cash_Page":
                log.logger.info("Entering to Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID number for Battery Product")
                quote_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_TEXT)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_array.append(number)
                max_index = quote_array.index(max(quote_array))
                quote_id_value = max(quote_array)
                # print("Array in Quote Page is ", quote_array)

                if quote_id_value is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_value} for Battery Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    quote_ID = self.driver.find_elements(
                        By.XPATH, GCS.QUOTE_IDS)
                    quote_ID_arr = []
                    for i in range(len(quote_ID)):
                        quote_ids_text = self.driver.find_element(
                            By.XPATH, GCS.quote_ids(i + 1)).text
                        q_number = quote_ids_text.split()[-1]
                        quote_ID_arr.append(q_number)
                    quote_ID_contract_page = max(quote_ID_arr)
                    if quote_id_value == quote_ID_contract_page:
                        log.logger.info(
                            f"Validation completed for Quote Number with generated quote number as {quote_ID_contract_page} for Battery Product ")
                        log.logger.info(
                            "Validating Contract Page Documents for Battery-Cash Product")
                        for i in range(1):
                            view_trinity_proposal_err = self.view_trinity_proposal(
                                quote_ID_contract_page)
                            if len(view_trinity_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(
                                    quote_ID_contract_page)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        quote_ID_contract_page)
                                    if len(view_combined_pack_err) > 0:
                                        break
                    else:
                        log.logger.error(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not matching for the Quote number  in contract page {quote_ID_contract_page} for Battery Product")
                        errors.append(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not matching for the Quote number  in contract page {quote_ID_contract_page} for Battery Product")

                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated as {quote_id_value} for Battery Product")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated as {quote_id_value} for Battery Product")
# TC-05***********************************************************************************************************************#
            if self.__class__.__name__ == "RRR_Sunnova_Page":
                log.logger.info("Entering to RRR Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for RRR")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_rrr = self.driver.find_element(By.XPATH,
                                                             GQS.system_id_following_quote(max_index + 1)).text
                else:
                    system_id_rrr = self.driver.find_element(By.XPATH,
                                                             GQS.system_id_following_quote(max_index)).text
                if system_id_rrr != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_rrr} for RRR")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # print("System ID Generated for RRR Sunnova Product", system_id_rrr)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for RRR-Sunnova Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_rrr)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_rrr)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_rrr)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_rrr)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        view_roof_proposal_err = self.view_roof_proposal(
                                            system_id_rrr)
                                        if len(view_roof_proposal_err) > 0:
                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID is not generated for this Quote and is generated as {system_id_rrr} for RRR")
                    errors.append(
                        f"Test Failed!!, System ID is not generated for this Quote and is generated as {system_id_rrr} for RRR")
# TC-06***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar-Sunnova Roof-Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Roof Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index + 1)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                # print("roof quote:", system_id_roof,
                #       "solar quote:", system_id_solar)
                if system_id_solar != "Quote Issue" and system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar"
                        f"and {system_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err_solar = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err_solar) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            "Validating Contract Page Documents for Roof Product")
                                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                            system_id_roof)
                                        if len(view_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                system_id_roof)
                                            if len(sign_finance_partner_proposal_err) > 0:
                                                break
                                            else:
                                                sfdc_sync_err = self.sfdc_sync(
                                                    system_id_roof)
                                                if len(sfdc_sync_err) > 0:
                                                    break
                                                else:
                                                    view_combined_pack_err = self.view_combined_pack(
                                                        system_id_roof)
                                                    if len(view_combined_pack_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Solar is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for Solar and {system_id_roof} for Roof")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Solar is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for Solar and {system_id_roof} for Roof")
# TC-07***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova Roof Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for Roof")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                # print("Quote page system id array", sys_array)

                if system_id_solar != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} and {quote_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            f"Moving Quote to Agreements since System ID is generated as {quote_id_roof} for Roof")
                                        log.logger.info(
                                            "Validating Contract Page Documents for Roof Product")
                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                            quote_id_roof)
                                        if len(view_trinity_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                quote_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    quote_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof and {system_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof and {system_id_solar} for Solar")
# TC-08***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text

                quote_id_battery = id_batt.split()[1]

                if system_id_solar != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar and"
                        f" {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            f"Moving Quote to Agreements since System ID is generated as {quote_id_battery} for Roof")
                                        log.logger.info(
                                            "Validating Contract Page Documents for Battery Product")
                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                            quote_id_battery)
                                        if len(view_trinity_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                quote_id_battery)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    quote_id_battery)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-09***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar-Sunnova RRR-Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and RRR Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index + 1)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                # print("roof quote:", system_id_roof,
                #       "solar quote:", system_id_solar)
                if system_id_solar != "Quote Issue" and system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar and {system_id_roof} for "
                        f"RRR")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(system_id_value)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    # print("System ID Generated for RRR Sunnova Product",
                    #       system_id_roof)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for Roof")
                                        log.logger.info(
                                            "Validating Contract Page Documents for Roof Product")
                                        self.driver.execute_script(
                                            "window.scrollTo(0, 0);")
                                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                            system_id_roof)
                                        if len(view_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                system_id_roof)
                                            if len(sign_finance_partner_proposal_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break

                else:
                    log.logger.error(
                        f"Test Failed!!, System ID is not generated for this Quote and is generated as"
                        f"{system_id_solar} for Solar and {system_id_roof} for Roof ")
                    errors.append(
                        "Test Failed!!, System ID is not generated for this Quote")
# TC-10***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Cash_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova, Roof Cash and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for Roof and Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    # Convert to integers for sorting
                    sys_array.append(int(number))
                sys_array.sort(reverse=True)  # Sort the array
                # Find max index after sorting
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                # print("max_index", max_index)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_batt.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]

                if system_id_solar != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar,"
                        f"{quote_id_roof} for Roof and {quote_id_battery} for Battery")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)

                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            "Validating Contract Page Documents for Roof Product")
                                        self.driver.execute_script(
                                            "window.scrollTo(0, 0);")
                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                            quote_id_roof)
                                        if len(view_trinity_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                quote_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    quote_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    log.logger.info(
                                                        "Validating Contract Page Documents for Battery Product")
                                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                                        quote_id_battery)
                                                    if len(view_trinity_proposal_err) > 0:
                                                        break
                                                    else:
                                                        sfdc_sync_err = self.sfdc_sync(
                                                            quote_id_battery)
                                                        if len(sfdc_sync_err) > 0:
                                                            break
                                                        else:
                                                            view_combined_pack_err = self.view_combined_pack(
                                                                quote_id_battery)
                                                            if len(view_combined_pack_err) > 0:
                                                                break
                        # break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-11***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova Roof Sunnova Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Roof and QUote ID for Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index+1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                # print("roof quote:", system_id_roof,
                #       "solar quote:", system_id_solar)
                if system_id_solar != "Quote Issue" and system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar,"
                        f"{system_id_roof} for Roof and {quote_id_battery} for Battery")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(system_id_value)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for Roof")
                    log.logger.info(
                        "Validating Contract Page Documents for Roof Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_roof)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_roof)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_roof)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_roof)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        view_roof_proposal_err = self.view_roof_proposal(
                                            system_id_roof)
                                        if len(view_roof_proposal_err) > 0:
                                            break
                                        else:
                                            log.logger.info(
                                                "Validating Contract Page Documents for Battery Product")
                                            view_trinity_proposal_err = self.view_trinity_proposal(
                                                quote_id_battery)
                                            if len(view_trinity_proposal_err) > 0:
                                                break
                                            else:
                                                sfdc_sync_err = self.sfdc_sync(
                                                    quote_id_battery)
                                                if len(sfdc_sync_err) > 0:
                                                    break
                                                else:
                                                    view_combined_pack_err = self.view_combined_pack(
                                                        quote_id_battery)
                                                    if len(view_combined_pack_err) > 0:
                                                        break
                                                    else:
                                                        log.logger.info(
                                                            "Validating Contract Page Documents for Solar Product")
                                                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                                            system_id_solar)
                                                        if len(view_finance_partner_proposal_err) > 0:
                                                            break
                                                        else:
                                                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                                system_id_solar)
                                                            if len(sign_finance_partner_proposal_err) > 0:
                                                                break
                                                            else:
                                                                sfdc_sync_err = self.sfdc_sync(
                                                                    system_id_solar)
                                                                if len(sfdc_sync_err) > 0:
                                                                    break
                                                                else:
                                                                    view_combined_pack_err = self.view_combined_pack(
                                                                        system_id_solar)
                                                                    if len(view_combined_pack_err) > 0:
                                                                        break
                        # break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof/Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} Roof Roof, {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Roof/Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} Roof Roof, {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-12***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Cash_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova, RRR Cash and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for RRR and Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_batt.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]

                if system_id_solar != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar}, {quote_id_rrr} for RRR and "
                        f"{quote_id_battery} for Battery")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Battery Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_battery)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_battery)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_battery)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Solar Product")
                                                view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                                    system_id_solar)
                                                if len(view_finance_partner_proposal_err) > 0:
                                                    break
                                                else:
                                                    sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                        system_id_solar)
                                                    if len(sign_finance_partner_proposal_err) > 0:
                                                        break
                                                    else:
                                                        sfdc_sync_err = self.sfdc_sync(
                                                            system_id_solar)
                                                        if len(sfdc_sync_err) > 0:
                                                            break
                                                        else:
                                                            view_combined_pack_err = self.view_combined_pack(
                                                                system_id_solar)
                                                            if len(view_combined_pack_err) > 0:
                                                                break
                        # break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_rrr} for RRR, {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_rrr} for RRR, {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-13***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Cash_Page":
                log.logger.info(
                    "Entering to Solar Cash Roof Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar and Roof Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]

                if quote_id_solar is not None and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for "
                        f"Solar Product and {quote_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_roof} for Roof ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_roof} for Roof ")
# TC-14***********************************************************************************************************************#
            if self.__class__.__name__ == "Roof_Cash_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Roof Cash Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova Quote ID for Solar and Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]

                if quote_id_roof is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_battery} for Battery"
                        f" Product and {quote_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_battery)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_battery)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_battery)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_roof} for Roof and {quote_id_battery} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_roof} for Roof and {quote_id_battery} for Battery ")
# TC-15***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Cash_Page":
                log.logger.info(
                    "Entering to Solar Cash RRR Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar and RRR Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                if quote_id_solar is not None and quote_id_rrr is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_rrr} for RRR")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_rrr} for RRR ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_rrr} for RRR ")
# TC-16***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Cash, Roof Sunnova & Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created System ID for Roof and Quote ID for Solar and Battery ")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof, "battery quote:", quote_id_battery)

                if system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for Roof, {quote_id_solar} for Solar "
                        f"and {quote_id_battery} for Battery")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)

                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Battery Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_battery)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_battery)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_battery)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Roof Product")
                                                view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                                    system_id_roof)
                                                if len(view_finance_partner_proposal_err) > 0:
                                                    break
                                                else:
                                                    sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                        system_id_roof)
                                                    if len(sign_finance_partner_proposal_err) > 0:
                                                        break
                                                    else:
                                                        sfdc_sync_err = self.sfdc_sync(
                                                            system_id_roof)
                                                        if len(sfdc_sync_err) > 0:
                                                            break
                                                        else:
                                                            view_combined_pack_err = self.view_combined_pack(
                                                                system_id_roof)
                                                            if len(view_combined_pack_err) > 0:
                                                                break
                                                            else:
                                                                view_roof_proposal_err = self.view_roof_proposal(
                                                                    system_id_roof)
                                                                if len(view_roof_proposal_err) > 0:
                                                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-17***********************************************************************************************************************#
            if self.__class__.__name__ == "Rrr_Cash_Page":
                log.logger.info("Entering to RRR Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for RRR Product")
                quote_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_TEXT)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_array.append(number)
                max_index = quote_array.index(max(quote_array))
                quote_id_value = max(quote_array)
                # print("Array in Quote Page is ", quote_array)
                if quote_id_value is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_value} for RRR Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()

                    quote_ID = self.driver.find_elements(
                        By.XPATH, GCS.QUOTE_IDS)
                    quote_ID_arr = []
                    for i in range(len(quote_ID)):
                        quote_ids_text = self.driver.find_element(
                            By.XPATH, GCS.quote_ids(i + 1)).text
                        q_number = quote_ids_text.split()[-1]
                        quote_ID_arr.append(q_number)
                        quote_ID_contract_page = max(quote_ID_arr)
                    if quote_id_value == quote_ID_contract_page:
                        log.logger.info(
                            f"Validation completed for Quote Number with generated quote number as {quote_ID_contract_page} for RRR Product ")
                        log.logger.info(
                            "Validating Contract Page Documents for RRR-Cash Product")
                        for i in range(1):
                            view_trinity_proposal_err = self.view_trinity_proposal(
                                quote_ID_contract_page)
                            if len(view_trinity_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(
                                    quote_ID_contract_page)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        quote_ID_contract_page)
                                    if len(view_combined_pack_err) > 0:
                                        break
                    else:
                        log.logger.error(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for RRR "
                            f"Product")
                        errors.append(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for RRR "
                            f"Product")

                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and"
                        f" is generated as {quote_ID_contract_page} for RRR Product")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and"
                        f" is generated as {quote_ID_contract_page} for RRR Product")
# TC-18***********************************************************************************************************************#
            if self.__class__.__name__ == "Rrr_Service_Finance_Page":
                log.logger.info("Entering to RRR Service Finance  Page...")
                log.logger.info("Retrieving newly created Quote ID for RRR")
                quote_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_TEXT)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_array.append(number)
                max_index = quote_array.index(max(quote_array))
                quote_id_value = max(quote_array)
                # print("Array in Quote Page is ", quote_array)
                if quote_id_value is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_value} for RRR Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()

                    quote_ID = self.driver.find_elements(
                        By.XPATH, GCS.QUOTE_IDS)
                    quote_ID_arr = []
                    for i in range(len(quote_ID)):
                        quote_ids_text = self.driver.find_element(
                            By.XPATH, GCS.quote_ids(i + 1)).text
                        q_number = quote_ids_text.split()[-1]
                        quote_ID_arr.append(q_number)
                        quote_ID_contract_page = max(quote_ID_arr)
                    if quote_id_value == quote_ID_contract_page:
                        log.logger.info(
                            f"Validation completed for Quote Number with generated quote number as {quote_ID_contract_page} for RRR Product ")
                        log.logger.info(
                            "Validating Contract Page Documents for RRR-Service Finance Product")
                        for i in range(1):
                            view_trinity_proposal_err = self.view_trinity_proposal(
                                quote_ID_contract_page)
                            if len(view_trinity_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(
                                    quote_ID_contract_page)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        quote_ID_contract_page)
                                    if len(view_combined_pack_err) > 0:
                                        break
                    else:
                        log.logger.error(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for RRR "
                            f"Product")
                        errors.append(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for RRR "
                            f"Product")

                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this product, and is generated as"
                        f" {quote_ID_contract_page} for RRR Product")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this product, and is generated as"
                        f" {quote_ID_contract_page} for RRR Product")
# TC-19***********************************************************************************************************************#
            if self.__class__.__name__ == "Roof_Service_Finance_Page":
                log.logger.info("Entering to Roof Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Roof Product")
                quote_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_TEXT)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_array.append(number)
                # print(quote_array)
                max_index = quote_array.index(max(quote_array))
                quote_id_value = max(quote_array)
                if quote_id_value is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_value} for Roof Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    time.sleep(3)
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    quote_ID = self.driver.find_elements(
                        By.XPATH, GCS.QUOTE_IDS)
                    quote_ID_arr = []
                    for i in range(len(quote_ID)):
                        quote_ids_text = self.driver.find_element(
                            By.XPATH, GCS.quote_ids(i + 1)).text
                        q_number = quote_ids_text.split()[-1]
                        quote_ID_arr.append(q_number)
                    quote_ID_contract_page = max(quote_ID_arr)
                    if quote_id_value == quote_ID_contract_page:
                        log.logger.info(
                            f"Validation completed for Quote Number with generated quote number as {quote_ID_contract_page} for Roof Product ")
                        log.logger.info(
                            "Validating Contract Page Documents for Roof-Cash Product")
                        for i in range(1):
                            view_trinity_proposal_err = self.view_trinity_proposal(
                                quote_ID_contract_page)
                            if len(view_trinity_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(
                                    quote_ID_contract_page)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        quote_ID_contract_page)
                                    if len(view_combined_pack_err) > 0:
                                        break

                        # self.view_trinity_proposal(quote_ID_contract_page)
                        # self.sfdc_sync(quote_ID_contract_page)
                        # self.view_combined_pack(quote_ID_contract_page)

                    else:
                        log.logger.error(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for Roof "
                            f"Product")
                        errors.append(
                            f"Test Failed!!, Quote Number is generated from Generate Quote {quote_id_value} is not "
                            f"matching for the Quote number  in contract page {quote_ID_contract_page} for Roof "
                            f"Product")

                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as "
                        f"{quote_ID_contract_page} for Roof Product")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as "
                        f"{quote_ID_contract_page} for Roof Product")
# TC-20***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Page":
                log.logger.info(
                    "Entering to Solar Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar")
                quote_num_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_num_array.append(number)
                max_index = quote_num_array.index(max(quote_num_array))
                # print("Quote page system id array", quote_num_array)
                # print("max_index", max_index)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                quote_id_solar = id_solar.split()[1]
                if quote_id_solar is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated"
                        f" as {quote_id_solar}")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated"
                        f" as {quote_id_solar}")
# TC-21***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar Cash Roof Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created System ID for Roof and Quote ID for Solar")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)

                if system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for Roof"
                        f"and {quote_id_solar} for Solar")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)

                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")

                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_roof)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_roof)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_roof)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for Roof, {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for Roof, {quote_id_solar} for Solar")
# TC-22***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova RRR Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for RRR")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                max_index = sys_array.index(max(sys_array))
                sys_array.sort(reverse=True)
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]

                if system_id_solar != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar and {quote_id_rrr} for "
                        f"RRR")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    for i in range(1):
                        log.logger.info(
                            "Validating Contract Page Documents for RRR Product")
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_rrr)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(
                                quote_id_rrr)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_rrr)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Solar Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_solar)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_solar)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_solar)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_solar)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for Solar, {quote_id_rrr} for RRR")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for Solar, {quote_id_rrr} for RRR")
# TC-23***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Page":
                log.logger.info(
                    "Entering to Solar Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar")
                quote_num_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    quote_num_array.append(number)
                quote_num_array.sort(reverse=True)
                max_index = quote_num_array.index(max(quote_num_array))
                # print("Quote page system id array", quote_num_array)
                # print("max_index", max_index)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                quote_id_solar = id_solar.split()[1]
                if quote_id_solar is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote ID is not generated for this Quote, and is generated as {quote_id_solar}")
                    errors.append(
                        f"Test Failed!!, Quote ID is not generated for this Quote, and is generated as {quote_id_solar}")
# TC-24***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_service_finance_Rrr_service_finance_Page":
                log.logger.info(
                    "Entering to Solar Service Finance and  RRR Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote for Solar and RRR Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                if quote_id_solar is not None and quote_id_rrr is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} "
                        f"for Solar Product and {quote_id_rrr} for RRR")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_rrr} for RRR ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_rrr} for RRR ")
# TC-25***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Cash_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Cash, Roof Cash and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote for Solar, ROof and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]

                if quote_id_solar is not None and quote_id_roof is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_roof} for Roof and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar, {quote_id_roof} for Roof and {quote_id_battery} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar, {quote_id_roof} for Roof and {quote_id_battery} for Battery ")
# TC-26***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_service_finance_Roof_service_finance_Page":
                log.logger.info(
                    "Entering to Solar Service Finance and Roof Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote for Solar and Roof")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                if quote_id_solar is not None and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for "
                        f"Solar Product and {quote_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_roof} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_roof} for Battery ")
# TC-27***********************************************************************************************************************#
            if self.__class__.__name__ == "Roof_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Roof Sunnova Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Roof and Quote ID for Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index+1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                # print("roof quote:", system_id_roof,
                #       "solar quote:", system_id_solar)
                if system_id_roof != "Quote Issue" and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for Roof "
                        f"and Quote id for battery is {quote_id_battery} ")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Roof Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_roof)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_roof)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_roof)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_roof)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        view_roof_proposal_err = self.view_roof_proposal(
                                            system_id_roof)
                                        if len(view_roof_proposal_err) > 0:
                                            break
                                        else:
                                            log.logger.info(
                                                "Validating Contract Page Documents for Battery Product")
                                            view_trinity_proposal_err = self.view_trinity_proposal(
                                                quote_id_battery)
                                            if len(view_trinity_proposal_err) > 0:
                                                break
                                            else:
                                                sfdc_sync_err = self.sfdc_sync(
                                                    quote_id_battery)
                                                if len(sfdc_sync_err) > 0:
                                                    break
                                                else:
                                                    view_combined_pack_err = self.view_combined_pack(
                                                        quote_id_battery)
                                                    if len(view_combined_pack_err) > 0:
                                                        break
                        # break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for Roof and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for Roof and {quote_id_battery} for Battery")
# TC-28***********************************************************************************************************************#
            if self.__class__.__name__ == "Roof_Service_Finance_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Roof Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Roof and Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    # print("Quote page system id array", sys_array)
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                if quote_id_roof is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_roof} for Roof Product "
                        f"and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Roof Product")
                    view_trinity_proposal_err = self.view_trinity_proposal(
                        quote_id_roof)
                    for i in range(1):
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(
                                quote_id_roof)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_roof)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Battery Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_battery)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_battery)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_battery)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_roof} for Roof and {quote_id_battery} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_roof} for Roof and {quote_id_battery} for Battery ")
# TC-29***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Cash and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote IDs for Solar and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof, "battery quote:", quote_id_battery).

                if quote_id_solar is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for"
                        f" Solar Product and {quote_id_battery} for Battery")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)

                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")

                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Battery Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_battery)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_battery)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_battery)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_battery} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f"{quote_id_solar} for Solar and {quote_id_battery} for Battery ")
# TC-30***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Service_Finance_Page":
                log.logger.info(
                    "Entering to Solar Sunnova Roof Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for Roof")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]

                if system_id_solar != "Quote Issue" and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} and Quote "
                        f"ID for Roof is {quote_id_roof}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    for i in range(1):
                        log.logger.info(
                            "Validating Contract Page Documents for Roof Product")
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_roof)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(
                                quote_id_roof)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_roof)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Solar Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_solar)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_solar)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_solar)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_solar)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for RRR, {quote_id_roof} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof is not generated for this Quote, "
                        f"and is generated as {system_id_solar} for RRR, {quote_id_roof} for Solar")
# TC-31***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                if quote_id_solar is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product"
                        f" and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    view_trinity_proposal_err = self.view_trinity_proposal(
                        quote_id_solar)
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Battery Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_battery)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_battery)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_battery)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and "
                        f"is generated as {quote_id_battery} for Battery, {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and "
                        f"is generated as {quote_id_battery} for Battery, {quote_id_solar} for Solar")
# TC-32***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_service_finance_Page":
                log.logger.info(
                    "Entering to Solar Cash Roof Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar and Roof Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                if quote_id_solar is not None and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and "
                        f"is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and "
                        f"is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar")
# TC-33***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar Service Finance and Roof Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created System ID for Roof and Quote ID for Solar")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)
                if system_id_roof != "Quote Issue" and quote_id_solar is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} and quote id for "
                        f"Solar is {quote_id_solar}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_roof)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_roof)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_roof)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {quote_id_solar} for Solar")
# TC-34***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Cash_Page":
                log.logger.info(
                    "Entering to Solar Service Finance and Roof Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote for Solar and Roof")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                if quote_id_solar is not None and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_roof} for Roof")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    view_trinity_proposal_err = self.view_trinity_proposal(
                        quote_id_solar)
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        "Test Failed!!, Quote Number is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar")
                    errors.append(
                        "Test Failed!!, Quote Number is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar")
# TC-35***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Service_Finance_Page":
                log.logger.info(
                    "Entering to Solar Sunnova, RRR Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for RRR Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index+1)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                if system_id_solar != "Quote Issue" and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar and Quote ID "
                        f"for RRR is {quote_id_roof}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)
                    for i in range(1):
                        log.logger.info(
                            "Validating Contract Page Documents for RRR Product")
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_roof)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(
                                quote_id_roof)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_roof)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Solar Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_solar)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_solar)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_solar)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_solar)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for RRR, {system_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for RRR, {system_id_solar} for Solar")
# TC-36***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_RRR_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar Cash and RRR Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created System ID for RRR and Quote ID for Solar")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)

                if system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for RRR and {quote_id_solar}"
                        f"for Solar")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)

                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_roof)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_roof)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_roof)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for RRR or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for RRR or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {quote_id_solar} for Solar")
# TC-37***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_RRR_service_finance_Page":
                log.logger.info(
                    "Entering to Solar Cash and RRR Service Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar and RRR Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    # print("Quote page system id array", sys_array)
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                if quote_id_solar is not None and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product"
                        f" and {quote_id_roof} for RRR")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f" {quote_id_roof} for RRR and {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f" {quote_id_roof} for RRR and {quote_id_solar} for Solar")
# TC-38***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_RRR_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar Service Finance RRR Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created System ID for RRR and Quote ID for Solar")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)

                if system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} for RRR and "
                        f"{quote_id_solar} for Solar")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)

                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_roof)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_roof)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_roof)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR and {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR and {quote_id_solar} for Solar")
# TC-39***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_service_finance_Rrr_Cash_Page":
                log.logger.info(
                    "Entering to Solar Service Finance and RRR Cash Finance Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar and RRR Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                if quote_id_solar is not None and quote_id_rrr is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product and {quote_id_rrr} for RRR")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated as "
                        f"{quote_id_rrr} for RRR, {quote_id_solar} for Solar")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote, and is generated as "
                        f"{quote_id_rrr} for RRR, {quote_id_solar} for Solar")
# TC-40***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Roof_Service_Finance_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Cash, Roof Service Finance Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar, Roof and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                if quote_id_solar is not None and quote_id_roof is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_roof} for Roof and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f" {quote_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f" {quote_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery ")
# TC-41***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Roof_Service_Finance_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova, Roof Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for Roof and Battery")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    # Convert to integers for sorting
                    sys_array.append(int(number))
                sys_array.sort(reverse=True)  # Sort the array
                # Find max index after sorting
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                # print("max_index", max_index)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index + 1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index + 1)).text
                    quote_id_roof = id_roof.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                time.sleep(1)
                print("system_id_solar:", system_id_solar)
                if system_id_solar != "Quote Issue" and quote_id_battery is not None and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar, {quote_id_roof} for Roof"
                        f"and {quote_id_battery} for Battery")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    # print("System ID Generated for Solar Sunnova Product",
                    #       system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            "Validating Contract Page Documents for Roof Product")
                                        self.driver.execute_script(
                                            "window.scrollTo(0, 0);")
                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                            quote_id_roof)
                                        if len(view_trinity_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                quote_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    quote_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    log.logger.info(
                                                        "Validating Contract Page Documents for Battery Product")
                                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                                        quote_id_battery)
                                                    if len(view_trinity_proposal_err) > 0:
                                                        break
                                                    else:
                                                        sfdc_sync_err = self.sfdc_sync(
                                                            quote_id_battery)
                                                        if len(sfdc_sync_err) > 0:
                                                            break
                                                        else:
                                                            view_combined_pack_err = self.view_combined_pack(
                                                                quote_id_battery)
                                                            if len(view_combined_pack_err) > 0:
                                                                break
                        # break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for Roof/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-42***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Service Finance, Roof Sunnova and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created System ID for Roof and Quite IDs for Solar and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)  # Sort the array
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)
                if system_id_roof != "Quote Issue" and quote_id_solar is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_roof} and quote id for Solar is {quote_id_solar} and"
                        f"quote id for Battery is{quote_id_battery}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_roof)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_roof)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_roof)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_roof)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_roof)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                                                    else:
                                                        log.logger.info(
                                                            "Validating Contract Page Documents for Battery Product")
                                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                                            quote_id_battery)
                                                        if len(view_trinity_proposal_err) > 0:
                                                            break
                                                        else:
                                                            sfdc_sync_err = self.sfdc_sync(
                                                                quote_id_battery)
                                                            if len(sfdc_sync_err) > 0:
                                                                break
                                                            else:
                                                                view_combined_pack_err = self.view_combined_pack(
                                                                    quote_id_battery)
                                                                if len(view_combined_pack_err) > 0:
                                                                    break

                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-43***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Cash_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Service Finance, Roof Cash and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar, Roof and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)  # Sort the array
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]

                if quote_id_solar is not None and quote_id_roof is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_roof} for Roof and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    view_trinity_proposal_err = self.view_trinity_proposal(
                        quote_id_solar)
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                            if len(view_trinity_proposal_err) > 0:
                                                break
                                            else:
                                                sfdc_sync_err = self.sfdc_sync(
                                                    quote_id_battery)
                                                if len(sfdc_sync_err) > 0:
                                                    break
                                                else:
                                                    view_combined_pack_err = self.view_combined_pack(
                                                        quote_id_battery)
                                                    if len(view_combined_pack_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for RRR/Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for RRR/Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-44***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Roof_Service_Finance_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Service Finance, Roof Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar, Roof and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]
                if quote_id_solar is not None and quote_id_roof is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product and "
                        f"{quote_id_roof} for Roof and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Roof Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_roof)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_roof)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_roof)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote ID for Roof/Solar/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, Quote ID for Roof/Solar/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for Roof, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-45***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova, Roof Sunnova and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and RRR and Quote ID for Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index + 1)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    system_id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                if system_id_solar != "Quote Issue" and system_id_roof != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} for Solar, {system_id_roof} for RRR and "
                        f"{quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            "Validating Contract Page Documents for RRR Product")
                                        self.driver.execute_script(
                                            "window.scrollTo(0, 0);")
                                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                            system_id_roof)
                                        if len(view_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                system_id_roof)
                                            if len(sign_finance_partner_proposal_err) > 0:
                                                break
                                            else:
                                                sfdc_sync_err = self.sfdc_sync(
                                                    system_id_roof)
                                                if len(sfdc_sync_err) > 0:
                                                    break
                                                else:
                                                    view_combined_pack_err = self.view_combined_pack(
                                                        system_id_roof)
                                                    if len(view_combined_pack_err) > 0:
                                                        break
                                                    else:
                                                        view_roof_proposal_err = self.view_roof_proposal(
                                                            system_id_roof)
                                                        if len(view_roof_proposal_err) > 0:
                                                            break
                                                        else:
                                                            log.logger.info(
                                                                "Validating Contract Page Documents for Battery Product")
                                                            view_trinity_proposal_err = self.view_trinity_proposal(
                                                                quote_id_battery)
                                                            if len(view_trinity_proposal_err) > 0:
                                                                break
                                                            else:
                                                                sfdc_sync_err = self.sfdc_sync(
                                                                    quote_id_battery)
                                                                if len(sfdc_sync_err) > 0:
                                                                    break
                                                                else:
                                                                    view_combined_pack_err = self.view_combined_pack(
                                                                        quote_id_battery)
                                                                    if len(view_combined_pack_err) > 0:
                                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for RRR/Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for RRR/Solar or Quote ID for Battery is not generated for this Quote, "
                        f"and is generated as {system_id_roof} for RRR, {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-46***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Cash_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Cash, RRR Cash & Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote ID for Solar, RRR and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]

                if quote_id_solar is not None and quote_id_rrr is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product "
                        f"and {quote_id_rrr} for Roof and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        "Test Failed!!, Quote Number is not generated for this Quote fand is"
                        f" generated as {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        "Test Failed!!, Quote Number is not generated for this Quote fand is"
                        f" generated as {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-47***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Service_Finance_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Cash, RRR Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar, RRR and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]

                if quote_id_solar is not None and quote_id_rrr is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product and "
                        f"{quote_id_rrr} for RRR and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote ID for Solar/Battery/RRR is not generated for this Quote, "
                        f"and is generated as {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, Quote ID for Solar/Battery/RRR is not generated for this Quote, "
                        f"and is generated as {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-48***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_RRR_Service_Finance_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Sunnova RRR Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Solar and Quote ID for RRR and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index + 1)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index + 1)).text
                    quote_id_roof = id_roof.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    id_roof = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_roof = id_roof.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                if system_id_solar != "Quote Issue" and quote_id_roof is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_solar} and Quote ID for RRR is {quote_id_roof} and Quote ID for "
                        f"Battery is {quote_id_battery}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)
                    for i in range(1):
                        log.logger.info(
                            "Validating Contract Page Documents for Roof Product")
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_roof)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(
                                quote_id_roof)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_roof)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for Solar Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_solar)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_solar)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_solar)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_solar)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    log.logger.info(
                                                        "Validating Contract Page Documents for Battery Product")
                                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                                        quote_id_battery)
                                                    if len(view_trinity_proposal_err) > 0:
                                                        break
                                                    else:
                                                        sfdc_sync_err = self.sfdc_sync(
                                                            quote_id_battery)
                                                        if len(sfdc_sync_err) > 0:
                                                            break
                                                        else:
                                                            view_combined_pack_err = self.view_combined_pack(
                                                                quote_id_battery)
                                                            if len(view_combined_pack_err) > 0:
                                                                break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for RRR, {system_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Solar or Quote ID for RRR/Battery is not generated for this Quote, "
                        f"and is generated as {quote_id_roof} for RRR, {system_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-49***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Cash_Rrr_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Cash, RRR Sunnova and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created System ID for RRR and Quote number for Solar and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)  # Sort the array
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                    system_id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    system_id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)
                if system_id_rrr != "Quote Issue" and quote_id_solar is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_rrr} and quote id for Solar is {quote_id_solar} and"
                        f"quote id for Battery is{quote_id_battery}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_rrr)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_rrr)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_rrr)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_rrr)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_rrr)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                                                    else:
                                                        log.logger.info(
                                                            "Validating Contract Page Documents for Battery Product")
                                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                                            quote_id_battery)
                                                        if len(view_trinity_proposal_err) > 0:
                                                            break
                                                        else:
                                                            sfdc_sync_err = self.sfdc_sync(
                                                                quote_id_battery)
                                                            if len(sfdc_sync_err) > 0:
                                                                break
                                                            else:
                                                                view_combined_pack_err = self.view_combined_pack(
                                                                    quote_id_battery)
                                                                if len(view_combined_pack_err) > 0:
                                                                    break

                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for RRR or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for RRR or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-50***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Rrr_Cash_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Service Finance RRR Cash and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar, RRR and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]

                if quote_id_solar is not None and quote_id_rrr is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product and {quote_id_rrr} "
                        f"for RRR and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote for this Quote, "
                        f"and is generated as {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote for this Quote, "
                        f"and is generated as {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-51***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Rrr_Service_Finance_Battery_Cash":
                log.logger.info(
                    "Entering to Solar Service Finance RRR Service Finance and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created Quote number for Solar, RRR and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                if max_index == 0:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index+1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index+1)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index+1)).text
                    quote_id_battery = id_battery.split()[1]
                else:
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_cash_quote_section(max_index)).text
                    quote_id_rrr = id_rrr.split()[1]
                    id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_battery.split()[1]

                if quote_id_solar is not None and quote_id_rrr is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since Quote ID is generated as {quote_id_solar} for Solar Product and {quote_id_rrr} for "
                        f"RRR and {quote_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_trinity_proposal_err = self.view_trinity_proposal(
                                        quote_id_rrr)
                                    if len(view_trinity_proposal_err) > 0:
                                        break
                                    else:
                                        sfdc_sync_err = self.sfdc_sync(
                                            quote_id_rrr)
                                        if len(sfdc_sync_err) > 0:
                                            break
                                        else:
                                            view_combined_pack_err = self.view_combined_pack(
                                                quote_id_rrr)
                                            if len(view_combined_pack_err) > 0:
                                                break
                                            else:
                                                log.logger.info(
                                                    "Validating Contract Page Documents for Battery Product")
                                                view_trinity_proposal_err = self.view_trinity_proposal(
                                                    quote_id_battery)
                                                if len(view_trinity_proposal_err) > 0:
                                                    break
                                                else:
                                                    sfdc_sync_err = self.sfdc_sync(
                                                        quote_id_battery)
                                                    if len(sfdc_sync_err) > 0:
                                                        break
                                                    else:
                                                        view_combined_pack_err = self.view_combined_pack(
                                                            quote_id_battery)
                                                        if len(view_combined_pack_err) > 0:
                                                            break
                else:
                    log.logger.error(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f" {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery ")
                    errors.append(
                        f"Test Failed!!, Quote Number is not generated for this Quote and is generated as"
                        f" {quote_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery ")
# TC-52***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Service_Finance_Rrr_Sunnova_Battery_Cash_Page":
                log.logger.info(
                    "Entering to Solar Service Finance RRR Sunnova and Battery Cash Page...")
                log.logger.info(
                    "Retrieving newly created System IDs for RRR and Quote number for Solar and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)  # Sort the array
                max_index = sys_array.index(max(sys_array))
                # print("Quote page max index", max_index)
                if max_index == 0:
                    system_id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index + 1)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index + 1)).text
                    quote_id_solar = id_solar.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index + 1)).text
                    quote_id_battery = id_batt.split()[1]
                else:
                    system_id_rrr = self.driver.find_element(
                        By.XPATH, GQS.roof_quote_section(max_index)).text
                    id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_cash_quote_section(max_index)).text
                    quote_id_solar = id_solar.split()[1]
                    id_batt = self.driver.find_element(
                        By.XPATH, GQS.battery_quote_section(max_index)).text
                    quote_id_battery = id_batt.split()[1]
                # print("solar quote:", quote_id_solar, "roof quote:",
                #       system_id_roof)
                if system_id_rrr != "Quote Issue" and quote_id_solar is not None and quote_id_battery is not None:
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_rrr} for RRR and quote id for Solar is {quote_id_solar} and"
                        f"quote id for Battery is{quote_id_battery}")
                    scroll = "document.querySelector('input[id=\"quote-version-table-search-textbox\"]').scrollIntoView()"
                    self.driver.execute_script(scroll)
                    time.sleep(1)
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # self.get_sys_id(quote_id_roof)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_trinity_proposal_err = self.view_trinity_proposal(
                            quote_id_solar)
                        if len(view_trinity_proposal_err) > 0:
                            break
                        else:
                            sfdc_sync_err = self.sfdc_sync(quote_id_solar)
                            if len(sfdc_sync_err) > 0:
                                break
                            else:
                                view_combined_pack_err = self.view_combined_pack(
                                    quote_id_solar)
                                if len(view_combined_pack_err) > 0:
                                    break
                                else:
                                    log.logger.info(
                                        "Validating Contract Page Documents for RRR Product")
                                    view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                        system_id_rrr)
                                    if len(view_finance_partner_proposal_err) > 0:
                                        break
                                    else:
                                        sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                            system_id_rrr)
                                        if len(sign_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sfdc_sync_err = self.sfdc_sync(
                                                system_id_rrr)
                                            if len(sfdc_sync_err) > 0:
                                                break
                                            else:
                                                view_combined_pack_err = self.view_combined_pack(
                                                    system_id_rrr)
                                                if len(view_combined_pack_err) > 0:
                                                    break
                                                else:
                                                    view_roof_proposal_err = self.view_roof_proposal(
                                                        system_id_rrr)
                                                    if len(view_roof_proposal_err) > 0:
                                                        break
                                                    else:
                                                        log.logger.info(
                                                            "Validating Contract Page Documents for Battery Product")
                                                        view_trinity_proposal_err = self.view_trinity_proposal(
                                                            quote_id_battery)
                                                        if len(view_trinity_proposal_err) > 0:
                                                            break
                                                        else:
                                                            sfdc_sync_err = self.sfdc_sync(
                                                                quote_id_battery)
                                                            if len(sfdc_sync_err) > 0:
                                                                break
                                                            else:
                                                                view_combined_pack_err = self.view_combined_pack(
                                                                    quote_id_battery)
                                                                if len(view_combined_pack_err) > 0:
                                                                    break

                else:
                    log.logger.error(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID for Roof or Quote ID for Solar/Battery is not generated for this Quote, "
                        f"and is generated as {system_id_rrr} for RRR, {quote_id_solar} for Solar and {quote_id_battery} for Battery")
# TC-53***********************************************************************************************************************#
            if self.__class__.__name__ == "Battery_Sunnova_Page":
                log.logger.info("Entering to Battery Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System ID for Battery Product")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                max_index = sys_array.index(max(sys_array))
                # print("Quote page system id array", sys_array)
                system_id_battery = self.driver.find_element(
                    By.XPATH, GQS.system_id_following_quote(max_index + 1)).text
                if system_id_battery != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System ID is generated as {system_id_battery}")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    # print("System ID Generated for Solar Sunnova Product", system_id_solar)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Battery-Sunnova Product...")
                    for i in range(1):
                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                            system_id_battery)
                        if len(view_finance_partner_proposal_err) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_battery)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(
                                    system_id_battery)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_battery)
                                    if len(view_combined_pack_err) > 0:
                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID is not generated for this Quote, and it is generated as {system_id_battery}")
                    errors.append(
                        f"Test Failed!!, System ID is not generated for this Quote, and it is generated as {system_id_battery}")
# TC-54***********************************************************************************************************************#
            if self.__class__.__name__ == "Solar_Sunnova_Battery_Sunnova_Page":
                log.logger.info(
                    "Entering to Solar-Sunnova Battery-Sunnova Page...")
                log.logger.info(
                    "Retrieving newly created Sunnova System IDs for Solar and Battery Products")
                sys_array = []
                quote_num_len = self.driver.find_elements(
                    By.XPATH, GQS.QUOTE_NUMBER_LENGTH)
                for i in range(len(quote_num_len)):
                    quotes = self.driver.find_element(
                        By.XPATH, GQS.quotes_value(i + 1)).text
                    number = quotes.split()[1]
                    sys_array.append(number)
                sys_array.sort(reverse=True)
                max_index = sys_array.index(max(sys_array))
                if max_index == 0:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index + 1)).text
                    system_id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_sys_id_section(max_index + 1)).text
                else:
                    system_id_solar = self.driver.find_element(
                        By.XPATH, GQS.solar_quote_section(max_index)).text
                    system_id_battery = self.driver.find_element(
                        By.XPATH, GQS.battery_sys_id_section(max_index)).text
                print("battery quote:", system_id_battery,
                      "solar quote:", system_id_solar)
                if system_id_solar != "Quote Issue" and system_id_battery != "Quote Issue":
                    log.logger.info(
                        f"Moving Quote to Agreements since System IDs are generated as {system_id_battery} for Solar and {system_id_battery} for Battery")
                    move_cb = self.driver.find_element(
                        By.XPATH, GQS.move_to_contract_cb(max_index + 1))
                    move_cb.click()
                    self.button_click(OPS.NEXT)
                    self.agreement_page_popup()
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    log.logger.info(
                        "Validating Contract Page Documents for Solar Product")
                    for i in range(1):
                        view_finance_partner_proposal_err_solar = self.view_finance_partner_proposal(
                            system_id_solar)
                        if len(view_finance_partner_proposal_err_solar) > 0:
                            break
                        else:
                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                system_id_solar)
                            if len(sign_finance_partner_proposal_err) > 0:
                                break
                            else:
                                sfdc_sync_err = self.sfdc_sync(system_id_solar)
                                if len(sfdc_sync_err) > 0:
                                    break
                                else:
                                    view_combined_pack_err = self.view_combined_pack(
                                        system_id_solar)
                                    if len(view_combined_pack_err) > 0:
                                        break
                                    else:
                                        log.logger.info(
                                            "Validating Contract Page Documents for Battery Product")
                                        view_finance_partner_proposal_err = self.view_finance_partner_proposal(
                                            system_id_battery)
                                        if len(view_finance_partner_proposal_err) > 0:
                                            break
                                        else:
                                            sign_finance_partner_proposal_err = self.sign_finance_partner_proposal(
                                                system_id_battery)
                                            if len(sign_finance_partner_proposal_err) > 0:
                                                break
                                            else:
                                                sfdc_sync_err = self.sfdc_sync(
                                                    system_id_battery)
                                                if len(sfdc_sync_err) > 0:
                                                    break
                                                else:
                                                    view_combined_pack_err = self.view_combined_pack(
                                                        system_id_battery)
                                                    if len(view_combined_pack_err) > 0:
                                                        break
                else:
                    log.logger.error(
                        f"Test Failed!!, System ID is not generated for this Quote, it is generated as "
                        f"{system_id_solar} for Solar and {system_id_battery} for Battery")
                    errors.append(
                        f"Test Failed!!, System ID is not generated for this Quote, it is generated as "
                        f"{system_id_solar} for Solar and {system_id_battery} for Battery")
# ****************************************************************************************************************************#
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            log.logger.error(f"An error occurred: {str(e)}")
        return errors
