from pages.tc_04_battery_cash import Battery_Cash_Page
from behave import *

Battery_Cash_Page = Battery_Cash_Page.get_instance()


@then('Verify End to End Work flow of Product Battery with Cash as Finance Method')
def end_to_end_roof_sunnova(context):
    Battery_Cash_Page.end_to_end_battery_cash()
    errs = Battery_Cash_Page.error_arr()
    if len(errs) > 0:
        assert False, "\n".join(errs)
