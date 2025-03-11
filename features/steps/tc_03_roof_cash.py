from pages.tc_03_roof_cash import Roof_Cash_Page
from behave import *

Roof_Cash_Page = Roof_Cash_Page.get_instance()


@then('Verify End to End Work flow of Product Roof with Cash as Finance Method')
def end_to_end_roof_sunnova(context):
    Roof_Cash_Page.end_to_end_roof_cash()
    errs = Roof_Cash_Page.error_arr()
    if len(errs) > 0:
        assert False, "\n".join(errs)
