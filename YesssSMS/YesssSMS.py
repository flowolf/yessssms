#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Send SMS via yesss.at web interface with your yesss login and password."""
#
# @author: Florian Klien <flowolf@klienux.org>
#
# pylint not amused about package name
# pylint: disable-msg=C0103

import sys
import argparse
import logging
import configparser
from datetime import datetime
from contextlib import suppress
from os.path import abspath
from os.path import isfile
from os.path import expanduser

import requests

from YesssSMS.const import VERSION, HELP,\
                           _LOGIN_ERROR_STRING,\
                           _LOGIN_LOCKED_MESS,\
                           _LOGIN_LOCKED_MESS_ENG,\
                           _UNSUPPORTED_CHARS_STRING,\
                           _SMS_SENDING_SUCCESSFUL_STRING,\
                           CONFIG_FILE_CONTENT,\
                           PROVIDER_URLS

MAX_MESSAGE_LENGTH_STDIN = 3*160

# yesss.at responds with HTTP 200 on non successful login
LOGIN = None  # normally your phone number
PASSWD = None  # your password

# alternatively import passwd and number from external file
with suppress(ImportError):
    # pylint: disable-msg=E0611
    from secrets import LOGIN, PASSWD


class YesssSMS():
    """YesssSMS class for sending SMS via yesss.at website."""

    class NoRecipientError(ValueError):
        """empty recipient."""

        pass

    class EmptyMessageError(ValueError):
        """empty message."""

        pass

    class LoginError(ValueError):
        """login credentials not accepted."""

        pass

    class AccountSuspendedError(LoginError):
        """too many failed login tries, account suspended for one hour."""

        pass

    class SMSSendingError(RuntimeError):
        """error during sending."""

        pass

    class UnsupportedCharsError(ValueError):
        """yesss.at refused characters in message."""

        pass

    class UnsupportedProviderError(ValueError):
        """the provider is not in the PROVIDER_URLS dict"""

        pass

    def __init__(self, login=LOGIN, passwd=PASSWD, provider=None, custom_provider=None):
        """Initialize YesssSMS member variables."""
        self._version = VERSION
        if not provider:
            self._provider = 'YESSS'
        else:
            self._provider = provider

        # set urls from provider
        if custom_provider:
            URLS = custom_provider
        else:
            try:
                URLS = PROVIDER_URLS[self._provider]
            except KeyError:
                available_providers = list(PROVIDER_URLS.keys())
                error_mess = "provider ({}) is not known to YesssSMS, ".format(self._provider) + \
                    "try one of the following: {}".format(", ".join(available_providers))
                raise self.UnsupportedProviderError(error_mess)

        self._login_url = URLS['LOGIN_URL']
        self._logout_url = URLS['LOGOUT_URL']
        self._kontomanager = URLS['KONTOMANAGER_URL']
        self._websms_url = URLS['WEBSMS_URL']
        self._suspended = False
        self._logindata = {'login_rufnummer': login,
                           'login_passwort': passwd}

    def _login(self, session, get_request=False):
        """Return a session for yesss.at."""
        req = session.post(self._login_url, data=self._logindata)
        if _LOGIN_ERROR_STRING in req.text or \
                req.status_code == 403 or \
                req.url == self._login_url:
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

    def send(self, recipient, message):
        """Send an SMS."""
        if self._logindata['login_rufnummer'] is None or \
                self._logindata['login_passwort'] is None:
            err_mess = "YesssSMS: Login data required"
            raise self.LoginError(err_mess)
        if not recipient:
            raise self.NoRecipientError("YesssSMS: recipient number missing")
        if not isinstance(recipient, str):
            raise ValueError("YesssSMS: str expected as recipient number")
        if not message:
            raise self.EmptyMessageError("YesssSMS: message is empty")

        with self._login(requests.Session()) as sess:

            sms_data = {'to_nummer': recipient, 'nachricht': message}
            req = sess.post(self._websms_url, data=sms_data)

            if not (req.status_code == 200 or req.status_code == 302):
                raise self.SMSSendingError("YesssSMS: error sending SMS")

            if _UNSUPPORTED_CHARS_STRING in req.text:
                raise self.UnsupportedCharsError(
                    "YesssSMS: message contains unsupported character(s)")

            if _SMS_SENDING_SUCCESSFUL_STRING not in req.text:
                raise self.SMSSendingError("YesssSMS: error sending SMS")

            sess.get(self._logout_url)

    def version(self):
        """Get version of YesssSMS package."""
        return self._version

def version_info():
    """Display version information"""
    print("yessssms {}".format(YesssSMS().version()))

def print_config_file():
    """Print a sample config file, to pipe into a file"""
    print(CONFIG_FILE_CONTENT, end="")

def parse_args(args):
    """Parse arguments and return namespace"""
    parser = argparse.ArgumentParser(description=HELP['desc'])
    parser.add_argument('-t', '--to', dest='recipient', help=HELP['to_help'])
    parser.add_argument('-m', '--message', help=HELP['message'])
    parser.add_argument('-c', '--configfile', help=HELP['configfile'])
    parser.add_argument('-l', '--login', dest='login', help=HELP['login'])
    parser.add_argument('-p', '--password', dest='password', help=HELP['password'])
    parser.add_argument('--mvno', dest='provider', help=HELP['provider'])
    parser.add_argument('--version', action='store_true',
                        default=False, help=HELP['version'])
    parser.add_argument("--test", action='store_true',
                        default=False, help=HELP['test'])
    parser.add_argument("--print-config-file", action='store_true',
                        default=False, help=HELP['print-config-file'])
    if not args:
        parser.print_help()
        return None

    return parser.parse_args(args)

def cli(test=None):
    """Handle arguments for command line interface"""
    from YesssSMS.const import CONFIG_FILE_PATHS

    args = parse_args(sys.argv[1:])

    DEFAULT_RECIPIENT = None
    PROVIDER = None
    CUSTOM_PROVIDER_URLS = None

    if not args:
        return

    if args.provider:
        PROVIDER = args.provider

    if args.print_config_file:
        print_config_file()
        return
    if args.version:
        version_info()
        return

    if args.configfile:
        CONFIG_FILE_PATHS.append(args.configfile)

    for conffile in CONFIG_FILE_PATHS:
        conffile = expanduser(conffile)
        conffile = abspath(conffile)
        try:
            if not isfile(conffile): # check if file is there
                continue
            logging.debug("configfile ({}) found".format(conffile))
            config = configparser.ConfigParser()
            config.read(conffile)
            # pylint: disable-msg=W0621
            LOGIN = str(config.get('YESSSSMS', 'LOGIN'))
            PASSWD = str(config.get('YESSSSMS', 'PASSWD'))
            
            if config.has_option("YESSSSMS", "DEFAULT_TO"):
                DEFAULT_RECIPIENT = config.get('YESSSSMS', 'DEFAULT_TO')
            if config.has_option("YESSSSMS", "MVNO"):
                PROVIDER = config.get('YESSSSMS', 'MVNO')
            if config.has_option("YESSSSMS_PROVIDER_URLS", "LOGIN_URL"):
                CUSTOM_PROVIDER_URLS = {
                    'LOGIN_URL': config.get('YESSSSMS_PROVIDER_URLS', 'LOGIN_URL'),
                    'LOGOUT_URL': config.get('YESSSSMS_PROVIDER_URLS', 'LOGOUT_URL'),
                    'KONTOMANAGER_URL': config.get('YESSSSMS_PROVIDER_URLS', 'KONTOMANAGER_URL'),
                    'WEBSMS_URL': config.get('YESSSSMS_PROVIDER_URLS', 'WEBSMS_URL')
                    }
        except (KeyError, configparser.NoSectionError) as ex:
            print("settings not found: {} ({})".format(conffile, ex))

    if args.login and args.password:
        LOGIN = args.login
        PASSWD = args.password

    try:
        logging.debug("login: {}".format(LOGIN))
        LOGIN or PASSWD
        if CUSTOM_PROVIDER_URLS:
            sms = YesssSMS(LOGIN, PASSWD, custom_provider=CUSTOM_PROVIDER_URLS)
        elif PROVIDER:
            sms = YesssSMS(LOGIN, PASSWD, provider=PROVIDER)
        else:
            sms = YesssSMS(LOGIN, PASSWD)
    except UnboundLocalError:
        print("error: no username or password defined (use --help for help)")
        return

    if args.message == "-":
        message = ""
        for line in sys.stdin:
            message += line
            if len(message) > MAX_MESSAGE_LENGTH_STDIN:
                break
        message = message[:MAX_MESSAGE_LENGTH_STDIN] # maximum of 3 SMS if pipe is used
    else:
        message = args.message

    if args.test:
        message = message or "yessssms ("+ VERSION +\
                  ") test message at {}".format(datetime.now().isoformat())
        recipient = args.recipient or DEFAULT_RECIPIENT or LOGIN
        sms.send(recipient, message)
    else:
        sms.send(DEFAULT_RECIPIENT or args.recipient, message)
    if test:
        return (sms, args, message)


if __name__ == "__main__":
    cli()
