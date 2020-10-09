#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YesssSMS class to login and send SMS via yesss.at web interface."""
#
# @author: Florian Klien <flowolf@klienux.org>
#
# pylint not amused about package name
# pylint: disable-msg=C0103

from contextlib import suppress
from functools import wraps
from os import getenv

import requests

from YesssSMS.const import (
    PROVIDER_URLS,
    VERSION,
    _LOGIN_ERROR_STRING,
    _LOGIN_LOCKED_MESS,
    _LOGIN_LOCKED_MESS_ENG,
    _SMS_SENDING_SUCCESSFUL_STRING,
    _UNSUPPORTED_CHARS_STRING,
)


MAX_MESSAGE_LENGTH_STDIN = 3 * 160

# yesss.at responds with HTTP 200 on non successful login
LOGIN = None  # normally your phone number
PASSWD = None  # your password

# alternatively import passwd and number from external file
with suppress(ImportError):
    # pylint: disable-msg=E0611
    from secrets import LOGIN, PASSWD


def connection_error_handled(func):
    """Decorate and handle network connection issues."""

    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            raise YesssSMS.ConnectionError(
                "YesssSMS cannot connect to provider"
            ) from None

    return func_wrapper


class YesssSMS:
    """YesssSMS class for sending SMS via yesss.at website.

    You can provide a different provider than YESSS.
    available providers are:
    * yesss
    * billitel
    * educom
    * fenercell
    * georg
    * goood
    * kronemobile
    * kuriermobil
    * simfonie
    * teleplanet
    * wowww
    * yooopi

    to set a custom provider, supporting the Kontomanager 'API' set `custom_provider`=
    {`LOGIN_URL`: url, `LOGOUT_URL`: url, `KONTOMANAGER_URL`: url, `WEBSMS_URL`: url}.
    """

    # pylint: disable=too-many-instance-attributes

    class NoRecipientError(ValueError):
        """missing recipient."""

    class EmptyMessageError(ValueError):
        """empty message."""

    class LoginError(ValueError):
        """login credentials not accepted."""

    class MissingLoginCredentialsError(UnboundLocalError):
        """login credentials not accepted."""

    class AccountSuspendedError(LoginError):
        """too many failed login tries, account suspended for one hour."""

    class SMSSendingError(RuntimeError):
        """error during sending."""

    class UnsupportedCharsError(ValueError):
        """provider refused characters in message."""

    class UnsupportedProviderError(ValueError):
        """the provider is not in the PROVIDER_URLS dict."""

    class ConnectionError(requests.ConnectionError):
        """YesssSMS cannot connect to the provider."""

    def __init__(
        self, login=LOGIN, passwd=PASSWD, provider="yesss", custom_provider=None
    ):
        """Initialize YesssSMS."""
        self._version = VERSION
        self._provider = provider.lower()

        env_login = getenv("YESSSSMS_LOGIN", None)
        env_passwd = getenv("YESSSSMS_PASSWD", None)

        if (login is None or passwd is None) and (
            env_login is None or env_passwd is None
        ):
            raise self.MissingLoginCredentialsError()

        if env_login is not None and env_passwd is not None:
            login = env_login
            passwd = env_passwd

        # set urls from provider
        if custom_provider:
            urls = custom_provider
        else:
            if self._provider not in PROVIDER_URLS:
                available_providers = list(PROVIDER_URLS.keys())
                error_mess = "provider ({}) is not known to YesssSMS, ".format(
                    self._provider
                ) + "try one of the following: {}".format(
                    ", ".join(available_providers)
                )
                raise self.UnsupportedProviderError(error_mess)
            urls = PROVIDER_URLS[self._provider]

        self._login_url = urls["LOGIN_URL"]
        self._logout_url = urls["LOGOUT_URL"]
        self._kontomanager = urls["KONTOMANAGER_URL"]
        self._websms_url = urls["WEBSMS_URL"]
        self._suspended = False
        self._logindata = {"login_rufnummer": login, "login_passwort": passwd}

    def _login(self, session, get_request=False):
        """Return a session for provider.

        return session
        If get_request is True return (session, request)
        """
        req = session.post(self._login_url, data=self._logindata)
        if (
            _LOGIN_ERROR_STRING in req.text
            or req.status_code == 403
            or req.url == self._login_url
        ):
            err_mess = "YesssSMS: login failed, username or password wrong"

            if _LOGIN_LOCKED_MESS in req.text:
                err_mess += ", page says: " + _LOGIN_LOCKED_MESS_ENG
                self._suspended = True
                raise self.AccountSuspendedError(err_mess)
            raise self.LoginError(err_mess)

        self._suspended = False  # login worked

        return (session, req) if get_request else session

    def account_is_suspended(self):
        """Return if account is suspended."""
        return self._suspended

    @connection_error_handled
    def login_data_valid(self):
        """Check for working login data."""
        login_working = False
        try:
            with self._login(requests.Session()) as sess:
                sess.get(self._logout_url)
        except self.LoginError:
            pass
        else:
            login_working = True
        return login_working

    @connection_error_handled
    def send(self, recipient, message):
        """Send an SMS."""
        if not recipient:
            raise self.NoRecipientError("YesssSMS: recipient number missing")
        if not isinstance(recipient, str):
            raise ValueError("YesssSMS: str expected as recipient number")
        if not message:
            raise self.EmptyMessageError("YesssSMS: message is empty")

        with self._login(requests.Session()) as sess:

            sms_data = {"to_nummer": recipient, "nachricht": message}
            req = sess.post(self._websms_url, data=sms_data)

            if not (req.status_code == 200 or req.status_code == 302):
                raise self.SMSSendingError("YesssSMS: error sending SMS")

            if _UNSUPPORTED_CHARS_STRING in req.text:
                raise self.UnsupportedCharsError(
                    "YesssSMS: message contains unsupported character(s)"
                )

            if _SMS_SENDING_SUCCESSFUL_STRING not in req.text:
                raise self.SMSSendingError("YesssSMS: error sending SMS")

            sess.get(self._logout_url)

    def get_login_url(self):
        """Get provider's login URL."""
        return self._login_url

    def get_provider(self):
        """Get currently set provider."""
        return self._provider

    def version(self):
        """Get version of YesssSMS package."""
        return self._version
