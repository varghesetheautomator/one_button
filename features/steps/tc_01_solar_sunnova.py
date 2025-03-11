from pages.tc_01_solar_sunnova import Solar_Sunnova_Page
from behave import *

Solar_Sunnova_Page = Solar_Sunnova_Page.get_instance()


@then('Verify End to End Work flow of Product Solar with Sunnova as Finance Method')
def end_to_end_solar_sunnova(context):
    Solar_Sunnova_Page.end_to_end_solar_sunnova()
    errs = Solar_Sunnova_Page.error_arr()
    if len(errs) > 0:
        assert False, "\n".join(errs)
