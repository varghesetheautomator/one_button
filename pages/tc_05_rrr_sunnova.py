import logging
import time
from pages.base_page import errors
from datas.admin_data_config import admin_data_settings
from selenium.webdriver.support.ui import WebDriverWait
from pages.tc_02_roof_sunnova import Roof_Sunnova_Page
from selector.home_selectors import HomePageSelectors as HPS
from selector.opportunity_selectors import OpportunityPageSelectors as OPS
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datas.opportunity_ids_config import opportunity_id
from utils.log_utils import Logger
from utils.random_number_util import random_util
from selector.utility_selectors import UtilityPageSelectors as UPS

log = Logger(__name__, logging.INFO)

random_num = random_util()


class RRR_Sunnova_Page(Roof_Sunnova_Page):
    """Object to represent the one button login page"""
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = RRR_Sunnova_Page()
        return cls.instance

    def __init__(self):
        super().__init__()

    def end_to_end_rrr_sunnova(self):
        try:

            log.logger.info(
                "Started Test for End to End Workflow of Product RRR with Sunnova as Finance Method")
            fetch_opportunity_err = self.fetch_opportunity(
                opportunity_id.RRR_SUNNOVA)
            for i in range(1):
                if len(fetch_opportunity_err) > 0:
                    errors.append(str(fetch_opportunity_err))
                else:
                    opportunity_page_error_validation_err = self.opportunity_page_error_validation()
                    if len(opportunity_page_error_validation_err) > 0:
                        errors.append(
                            str(opportunity_page_error_validation_err))
                    else:
                        check_product_and_fin_method_err = self.check_product_and_fin_method(
                            opportunity_id.RRR_SUNNOVA)
                        if len(check_product_and_fin_method_err) > 0:
                            errors.append(
                                str(check_product_and_fin_method_err))
                        else:
                            sunnova_sync_err = self.sunnova_sync()
                            if len(sunnova_sync_err) > 0:
                                errors.append(str(sunnova_sync_err))
                            else:
                                opportunity_page_err = self.opportunity_page()
                                if len(opportunity_page_err) > 0:
                                    errors.append(str(opportunity_page_err))
                                else:
                                    system_design_err = self.system_design()
                                    if len(system_design_err) > 0:
                                        errors.append(str(system_design_err))
                                    else:
                                        generate_quote_err = self.generate_quote_and_agreement_validations()
                                        if len(generate_quote_err) > 0:
                                            errors.append(
                                                str(generate_quote_err))
                break
            log.logger.info(
                "Completed Test for End to End Work flow of Product RRR with Sunnova as Finance"
                " Method")

        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")

    def error_arr(self):
        return errors
