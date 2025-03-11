import logging
from pages.base_page import errors, Page
from datas.opportunity_ids_config import opportunity_id
from utils.log_utils import Logger
from utils.random_number_util import random_util
from pages.tc_01_solar_sunnova import Solar_Sunnova_Page
log = Logger(__name__, logging.INFO)

random_num = random_util()


class Battery_Cash_Page(Solar_Sunnova_Page):
    """Object to represent the one button login page"""
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = Battery_Cash_Page()
        return cls.instance

    def __init__(self):
        super().__init__()

    def end_to_end_battery_cash(self):
        try:

            log.logger.info(
                "Started Test for End to End Workflow of Product Battery with Cash as Finance Method")

            fetch_opportunity_err = self.fetch_opportunity(
                opportunity_id.BATTERY_CASH)
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
                            opportunity_id.BATTERY_CASH)
                        if len(check_product_and_fin_method_err) > 0:
                            errors.append(
                                str(check_product_and_fin_method_err))
                        else:
                            black_knight_sync_err = self.black_knight_sync()
                            if len(black_knight_sync_err) > 0:
                                errors.append(str(black_knight_sync_err))
                            else:
                                opportunity_page_err = self.opportunity_page()
                                if len(opportunity_page_err) > 0:
                                    errors.append(str(opportunity_page_err))
                                else:
                                    utility_page_err = self.utility_page()
                                    if len(utility_page_err) > 0:
                                        errors.append(str(utility_page_err))
                                    else:
                                        system_design_err = self.system_design()
                                        if len(system_design_err) > 0:
                                            errors.append(
                                                str(system_design_err))
                                        else:
                                            generate_quote_err = self.generate_quote_and_agreement_validations()
                                            if len(generate_quote_err) > 0:
                                                errors.append(
                                                    str(generate_quote_err))
                break
            log.logger.info(
                "Completed Test for End to End Workflow of Product Battery with Cash as Finance Method")
        except Exception as e:
            errors.append(f"An exception occurred: {str(e)}")
            log.logger.error(f"An exception occurred: {str(e)}")

    def error_arr(self):
        return errors
