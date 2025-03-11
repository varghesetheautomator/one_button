from pages.tc_02_roof_sunnova import Roof_Sunnova_Page
from behave import *

Roof_Sunnova_Page = Roof_Sunnova_Page.get_instance()


@then('Verify End to End Work flow of Product Roof with Sunnova as Finance Method')
def end_to_end_roof_sunnova(context):
    Roof_Sunnova_Page.end_to_end_roof_sunnova()
    errs = Roof_Sunnova_Page.error_arr()
    if len(errs) > 0:
        assert False, "\n".join(errs)
