import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from tests.data.test_data import (
    host_api,
    host_mailhog,
    login,
    password,
    email,
)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            sort_keys=True,


        )
    ]
)
def test_post_v1_account():
    # 1. Register new user
    mailhog_configuration = MailhogConfiguration(host=host_mailhog,disable_log=True)
    dm_api_configuration = DmApiConfiguration(host=host_api,disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account,mailhog=mailhog)
    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)


