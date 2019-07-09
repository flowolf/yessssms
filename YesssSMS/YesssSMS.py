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
                           CONFIG_FILE_CONTENT

_LOGIN_URL = "https://www.yesss.at/kontomanager.at/index.php"
_LOGOUT_URL = "https://www.yesss.at/kontomanager.at/index.php?dologout=2"
_KONTOMANAGER_URL = "https://www.yesss.at/kontomanager.at/kundendaten.php"
_WEBSMS_URL = "https://www.yesss.at/kontomanager.at/websms_send.php"

# yesss.at responds with HTTP 200 on non successful login
YESSS_LOGIN = None  # normally your phone number
YESSS_PASSWD = None  # your password

# alternatively import passwd and number from external file
with suppress(ImportError):
    # pylint: disable-msg=E0611
    from secrets import YESSS_LOGIN, YESSS_PASSWD


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

    def __init__(self, yesss_login=YESSS_LOGIN, yesss_pw=YESSS_PASSWD):
        """Initialize YesssSMS member variables."""
        self._version = VERSION
        self._login_url = _LOGIN_URL
        self._logout_url = _LOGOUT_URL
        self._kontomanager = _KONTOMANAGER_URL
        self._websms_url = _WEBSMS_URL
        self._suspended = False
        self._logindata = {'login_rufnummer': yesss_login,
                           'login_passwort': yesss_pw}

    def _login(self, session, get_request=False):
        """Return a session for yesss.at."""
        req = session.post(self._login_url, data=self._logindata)
        if _LOGIN_ERROR_STRING in req.text or \
                req.status_code == 403 or \
                req.url == _LOGIN_URL:
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

def cli():
    """Handle arguments for command line interface"""
    from YesssSMS.const import CONFIG_FILE_PATHS

    args = parse_args(sys.argv[1:])

    DEFAULT_RECIPIENT = None

    if not args:
        return

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
            config = configparser.ConfigParser()
            config.read(conffile)
            # pylint: disable-msg=W0621
            YESSS_LOGIN = str(config.get('YESSS_AT', 'YESSS_LOGIN'))
            YESSS_PASSWD = str(config.get('YESSS_AT', 'YESSS_PASSWD'))
            if config.has_option("YESSS_AT", "YESSS_TO"):
                DEFAULT_RECIPIENT = config.get('YESSS_AT', 'YESSS_TO')
        except (KeyError, configparser.NoSectionError) as ex:
            print("settings not found: {} ({})".format(conffile, ex))

    if args.login and args.password:
        YESSS_LOGIN = args.login
        YESSS_PASSWD = args.password

    try:
        YESSS_LOGIN or YESSS_PASSWD
    except UnboundLocalError:
        print("error: no username or password defined (use --help for help)")
        return

    sms = YesssSMS(YESSS_LOGIN, YESSS_PASSWD)

    if args.test:
        message = args.message or "yessssms ("+ VERSION +\
                  ") test message at {}".format(datetime.now().isoformat())
        recipient = args.recipient or DEFAULT_RECIPIENT or YESSS_LOGIN
        sms.send(recipient, message)
    else:
        sms.send(DEFAULT_RECIPIENT or args.recipient, args.message)


if __name__ == "__main__":
    cli()
