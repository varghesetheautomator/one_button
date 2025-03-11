from pages.tc_05_rrr_sunnova import RRR_Sunnova_Page
from behave import *

RRR_Sunnova_Page = RRR_Sunnova_Page.get_instance()


@then('Verify End to End Work flow of Product RRR with Sunnova as Finance Method')
def end_to_end_roof_sunnova(context):
    RRR_Sunnova_Page.end_to_end_rrr_sunnova()
    errs = RRR_Sunnova_Page.error_arr()
    if len(errs) > 0:
        assert False, "\n".join(errs)
