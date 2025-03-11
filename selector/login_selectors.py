class LoginPageSelectors:
    USERNAME = "//input[@name='loginfmt']"
    NEXT_BUTTON = "//input[@type='submit']"
    PASSWORD = "//input[@name='passwd']"
    SIGN_BUTTON = "//input[@type='submit']"
    OK_BUTTON = "//input[@data-report-event='Signin_Submit']"
    NAMES = "//app-opportunity-id-admin//a"
    NAME_SORT = "(//button[@class='sorting-button'])[1]"

    USERNAME_CSS = "input[name='loginfmt']"
    NEXT_BUTTON_CSS = "input[type='submit']"
    PASSWORD_CSS = "input[name='passwd']"
    SIGN_BUTTON_CSS = "input[type='submit']"
    OK_BUTTON_CSS = "input[data-report-event='Signin_Submit']"

    USERNAME_ERROR = "//div[@id='usernameError']"
    PASSWORD_ERROR = "//div[@id='passwordError']"
