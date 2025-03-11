from behave import given, when, then
from context.config import settings
from context.driver import driver
from pages.login_page import LoginPage
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os
import logging
from utils.log_utils import Logger

load_dotenv()

errors = []
log = Logger(__name__, logging.INFO)

client_id = os.environ['AZURE_CLIENT_ID']
tenant_id = os.environ['AZURE_TENANT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
vault_url = os.environ["AZURE_KEYVAULT_URL"]
secret_name = os.environ["secret_name"]
secret_pass = os.environ["secret_pass"]

# create a credential
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)
# create a secret client object
secret_client = SecretClient(vault_url=vault_url, credential=credentials)

try:

    # retrieve the secret value from key vault
    secret_username = secret_client.get_secret(secret_name).value
    if not secret_username == "":
        log.logger.info("Username Retrieved Successfully from the Vault")
        secret_password = secret_client.get_secret(secret_pass).value
        if not secret_password == "":
            log.logger.info("Password Retrieved Successfully from the Vault")
        else:
            log.logger.error(
                "Password retrieve from Azure is showing as Blank")
            errors.append("Password retrieve from Azure is showing as Blank")
    else:
        errors.append("Username retrieve from Azure is showing as Blank")
        log.logger.error("Username retrieve from Azure is showing as Blank")

except Exception as e:
    log.logger.error(
        f"Error retrieving secret username or password from Azure Key Vault: {e}")
    errors.append(
        f"Error retrieving secret username or password from Azure Key Vault: {e}")


@given(u'I load the website')
def load_website(context):
    driver.navigate(settings.url)
    driver.get_driver().maximize_window()


@when('I login the page successfully')
def login(context):
    role = settings.role
    login_page = LoginPage.get_instance()

    if role == "admin":
        try:
            username = secret_username
            password = secret_password
            login_page.enter_username(username)
            errors = login_page.click_on_next_button()
            if len(errors) > 0:
                log.logger.error(
                    "Error occurred after entering the username. Aborting login process.")
                errors.append(
                    "Error occurred after entering the username. Aborting login process.")
                # Abort further login process if there's an error after entering the username
                assert False, "\n".join(errors)
            else:
                login_page.enter_password(password)
                login_page.click_on_sign_in_button()
                login_page.click_on_yes_button()
        except Exception as e:
            log.logger.error(
                f"Error occurred after entering the username or password. Aborting login process: {e}")
            errors.append(
                f"Error occurred after entering the username or password. Aborting login process: {e}")
            # Raise an exception to fail the scenario
            raise RuntimeError(
                "Test Failed, Username or Password Failed. Aborting login process")
