class GenerateContractPage:
    """Class for One Button Generate Contract Page"""

    POPUP_OK = "//span[normalize-space()='Ok']"
    POPUP_CANCEL = "//span[normalize-space()='Cancel']"
    PROCEED_POP_UP = "//span[normalize-space()='Proceed']"
    CONTRACT_PAGE = "//div[text()='Generate Sunnova Contract']"
    BATTERY_CASH_CONTRACT_PAGE = "//div[text()='Generate Cash/Service Finance Contract']"
    CONTRACT_PAGE_SYNC_ERROR = "//div[@id='syncSunnovaCheckListSection']//p[contains(@class, 'danger')]"
    CLOSE_ERROR = "(//button[@class='close'])[1]"
    SYSTEM_IDS = "//div[@col-id='SystemId' and @role='gridcell']"
    VIEW_PROPOSAL_SOLAR_FILE_CLICK_HERE = "//a[text()='Click here']"
    VIEW_PROPOSAL_SOLAR_MESSAGE = "(//div[contains(@class, 'ant-modal-content')]//b)[3]"
    CLOSE_BTN = "//i[contains(@class, 'close-icon')]"
    GENERATE_SUNNOVA_CONTRACT_BTN = "//button[text()='Generate Contract']"
    SIGN_FINANCE_PARTNER_CONTRACT_ERROR = "//div[contains(@class, 'ant-modal-content')]//div[contains(@class, 'danger')]"
    SIGN_FINANCE_PARTNER_CONTRACT_SUCCESS = "//div[text()=' The Loan contract was generated successfully. ']"
    CLICK_HERE = "//a[text()='Click here']"

    def system_ids(id):
        el = f"(//div[@col-id='SystemId' and @role='gridcell'])[{id}]"
        return el

    def proposal(id):
        el = f"(//a[@title='View Proposal'])[{id}]"
        return el

    QUOTE_IDS = "//div[@col-id='TrinityContractStatus' and @role='gridcell']"

    def quote_ids(id):
        el = f"(//div[@col-id='TrinityContractStatus' and @role='gridcell'])[{id}]"
        return el

    def view_trinity_proposal(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'View Trinity Proposal')][1]"
        return el

    def view_finance_partner_agreement(id):
        el = f"//*[contains(text(), '{id}')]/following::a[@title='View Finance Partner Agreement'][1]"
        return el

    def sign_finance_partner_contract_null(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'Sunnova Contract - null')][1]"
        return el

    def sign_finance_partner_proposal_gen(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'Sunnova Contract - Generated')][1]"
        return el

    def sign_finance_partner_contract(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'Sunnova Contract')][1]"
        return el

    def sfdc_sync(id):
        el = f"//*[contains(text(), '{id}')]/following::button[contains(@title, 'SFDC Sync')][1]"
        return el

    def view_combined_pack(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'View Combined Pack')][1]"
        return el

    def sign_combined_pack(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'Create Trinity Contract')][1]"
        return el

    def view_roof_proposal(id):
        el = f"//*[contains(text(), '{id}')]/following::a[contains(@title, 'View Roof Proposal')][1]"
        return el
