class UtilityPageSelectors:
    """Class for One Button Utility Page"""
    UTILITY_INFORMATION_TEXT = "//div[contains(text(),'Utility Information')]"
    UTILITY_BILL_NOT_SELECTED = "//b[text()='No contact on utility bill selected']"
    ANNUAL_USAGE_ERROR = "//div[contains(text(),'Annual Usage is required')]"
    ANNUAL_USAGE_INPUT = "//input[@formcontrolname='annualUsage']"
    UTILITY_SAVE = "//button//span[normalize-space()='SAVE']"
    LOAD_CALC_TAB = "//div[text()= 'Load Calculator']"
    LOAD_ITEMS_COUNT = "//div[@id='nav-loadcalculator']//input"
    EST_ANNUAL_USAGE = "//label[@class='total-text']//span"

    def load_calc_input(id):
        el = f"(//div[@id='nav-loadcalculator']//input)[{id}]"
        return el
