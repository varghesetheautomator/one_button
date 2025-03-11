class GenerateQuotePage:
    """Class for One Button Generate Quote Page"""
    QUOTE_SUMMARY_POPUP = "//div[contains(@class, 'ant-modal-content')]//div[text()='Quote Summary Data']"
    CANCEL_QUOTE_SUMMARY_POPUP = "//span[contains(text(),'Cancel')]"
    SYNC_WITH_SUNNOVA_POPUP = "//div[contains(@class, 'ant-modal-content')]//div[text()='Syncing with Sunnova']"
    FINANCE_PARTNER = "//select[@id='solar-detail-form-FinancePartnerId']"
    FINANCE_METHOD = "//select[@id='solar-detail-form-FinanceMethodId']"
    DESIRED_PPW = "//input[@id='solar-detail-form-DesiredPPWNet']"
    GENERATE_QUOTE = "//button[@id='generate-quote-button']"
    GENERATE_QUOTE_CSS = "button[id='generate-quote-button']"
    GENERATE_QUOTE_BTN_MENU = "(//span[normalize-space()='Generate Quote'])[1]"

    EXCEL_ICON = "//button[@class='excel-button ng-star-inserted']"
    CLOSE_EXCEl_POPUP = "//button[@class='close-button']"
    GENERATE_QUOTE_BTN_MENU_CSS = "button[class='ant-btn btnActive']"

    SELECT_ROOF_ADDER_TYPE = "//select[@id='roof-adder-type-dropdown']"
    SELECT_ROOF_PLUS_ICON = "//i[@class='fa fa-plus']"
    SELECT_ROOF_PLUS_ICON_CSS = "i[class='fa fa-plus']"
    ROOF_ADDER_COST_SUBTOTAL = "//span[text()='Adder Price Subtotal: ']/following::b"

    def solar_quote_section(max_index):
        el = f"(//label[text()='Solar Quote']/following::span[2])[{max_index}]"
        return el

    def roof_quote_section(max_index):
        el = f"(//label[text()='Roof Quote']/following::span[2])[{max_index}]"
        return el

    def battery_sys_id_section(max_index):
        el = f"(//label[text()='Battery Quote']/following::span[2])[{max_index}]"
        return el

    def quotes_value(id):
        el = f"(//div[@id='QuoteVersionsBody']//label[contains(text(), '#')])[{id}]"
        return el

    def system_id_following_quote(max_index):
        el = f"(//div[@id='QuoteVersionsBody']//a[contains(@class, 'quote-')])[{max_index}]"
        return el

    def move_to_contract_cb(max_index):
        el = f"(//div[@id='QuoteVersionsBody']//input[@type='checkbox'])[{max_index}]"
        return el

    def solar_cash_quote_section(max_index):
        el = f"(//label[text()='Solar Quote']/following::label[1])[{max_index}]"
        return el

    def roof_cash_quote_section(max_index):
        el = f"(//label[text()='Roof Quote']/following::label[1])[{max_index}]"
        return el

    def battery_quote_section(max_index):
        el = f"(//label[text()='Battery Quote']/following::label[1])[{max_index}]"
        return el

    def enter_adder_val(id):
        el = f"(//input[@type='number'])[{id}]"
        return el
