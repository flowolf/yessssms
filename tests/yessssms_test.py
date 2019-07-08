#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mocked tests for YesssSMS Module."""
import pytest
import requests
import requests_mock
import YesssSMS
from YesssSMS.YesssSMS import version_info, cli, print_config_file
from YesssSMS.const import VERSION, _UNSUPPORTED_CHARS_STRING

try:
    from secrets import YESSS_LOGIN, YESSS_PASSWD, YESSS_TO
except ImportError:
    YESSS_LOGIN = "06641234567"
    YESSS_PASSWD = "testpasswd"
    YESSS_TO = "06501234567"


def test_credentials_work():
    """Test for working credentials."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=302,
                          # pylint: disable=protected-access
                          headers={'location': sms._kontomanager}
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._kontomanager,
                          status_code=200,
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        assert sms.version() == VERSION
        print("user: {}, pass: {}, to: {}".format(
            YESSS_LOGIN, YESSS_PASSWD[0]+(len(YESSS_PASSWD)-1)*'*', YESSS_TO))
        assert sms.login_data_valid() is True
        # pylint: disable=protected-access
        assert isinstance(sms._logindata['login_rufnummer'], str)
        # pylint: disable=protected-access
        assert isinstance(sms._logindata['login_passwort'], str)
        # pylint: disable=protected-access
        assert len(sms._logindata['login_rufnummer']) > 10
        # pylint: disable=protected-access
        assert sms._logindata['login_passwort']


def test_login():
    """Test if login works."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=302,
                          # pylint: disable=protected-access
                          headers={'location': sms._kontomanager}
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._kontomanager,
                          status_code=200,
                          text="test..."+YESSS_LOGIN+"</a>"
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        # pylint: disable=protected-access
        session, request = sms._login(requests.Session(), get_request=True)
        # pylint: disable=protected-access
        session.get(sms._logout_url)
        # pylint: disable=protected-access
        assert sms._logindata['login_rufnummer'][-7:]+"</a>" in request.text
        # pylint: disable=protected-access
        assert request.url == sms._kontomanager


def test_empty_message():
    """Test error handling for empty message."""
    sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
    with pytest.raises(ValueError):
        sms.send(YESSS_TO, "")
    with pytest.raises(sms.EmptyMessageError):
        sms.send(YESSS_TO, "")


def test_login_error():
    """Test error handling of faulty login."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=200,
                          text="<strong>Login nicht erfolgreich"
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        with pytest.raises(sms.LoginError):
            sms.send(YESSS_TO, "test")


def test_login_empty_password_error():
    """Test error handling of empty password."""
    sms = YesssSMS.YesssSMS("0000000000", None)
    with pytest.raises(sms.LoginError):
        sms.send(YESSS_TO, "test")


def test_login_empty_login_error():
    """Test error handling of empty login."""
    sms = YesssSMS.YesssSMS("", "2d4faa0ea6f55813")
    with pytest.raises(sms.LoginError):
        sms.send(YESSS_TO, "test")


def test_no_recipient_error():
    """Test error handling of no recipient."""
    sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
    with pytest.raises(sms.NoRecipientError):
        sms.send("", "test")


def test_recipient_not_str_error():
    """Test error handling of wrong recipient data type."""
    sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
    with pytest.raises(ValueError):
        sms.send(176264916361239, "test")


def test_message_sending_error():
    """Test handling of status codes other than 200 and 302."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=302,
                          # pylint: disable=protected-access
                          headers={'location': sms._kontomanager}
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._kontomanager,
                          status_code=200,
                          )
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._websms_url,
                          status_code=400,
                          text="<h1>OOOOPS</h1>"
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        with pytest.raises(sms.SMSSendingError):
            sms.send(YESSS_TO, "test")


def test_unsupported_chars_error():
    """Test error handling for unsupported chars."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=302,
                          # pylint: disable=protected-access
                          headers={'location': sms._kontomanager}
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._kontomanager,
                          status_code=200,
                          )
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._websms_url,
                          status_code=200,
                          text=_UNSUPPORTED_CHARS_STRING
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        with pytest.raises(sms.UnsupportedCharsError):
            sms.send(YESSS_TO, "test")


def test_sms_sending_error():
    """Test error handling for missing success string."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=302,
                          # pylint: disable=protected-access
                          headers={'location': sms._kontomanager}
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._kontomanager,
                          status_code=200,
                          )
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._websms_url,
                          status_code=200,
                          text="some text i'm not looking for"
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        with pytest.raises(sms.SMSSendingError):
            sms.send(YESSS_TO, "test")


def test_login_suspended_error():
    """Test error handling for suspended account."""
    with requests_mock.Mocker() as mock:
        # non existing user and password
        sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=200,
                          text="<strong>Login nicht erfolgreich bla Wegen "
                               "3 ungültigen Login-Versuchen ist Ihr Account "
                               "für eine Stunde gesperrt."
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )

        assert sms.login_data_valid() is False
        # LoginError
        with pytest.raises(sms.AccountSuspendedError):
            sms.send(YESSS_TO, "test")
        assert sms.account_is_suspended() is True


def test_send_sms():
    """Test SMS sending."""
    with requests_mock.Mocker() as mock:
        sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._login_url,
                          status_code=302,
                          # pylint: disable=protected-access
                          headers={'location': sms._kontomanager}
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._kontomanager,
                          status_code=200,
                          )
        mock.register_uri('POST',
                          # pylint: disable=protected-access
                          sms._websms_url,
                          status_code=200,
                          text="<h1>Ihre SMS wurde erfolgreich " +
                               "verschickt!</h1>"
                          )
        mock.register_uri('GET',
                          # pylint: disable=protected-access
                          sms._logout_url,
                          status_code=200,
                          )
        try:
            sms.send(YESSS_TO, "testing YesssSMS version {}, seems to work! :)"
                     .format(sms.version()))
        except (ValueError, RuntimeError):
            pytest.fail("Exception raised while sending SMS")

def test_cli_print_config_file(capsys):
    """test for correct config file output"""
    print_config_file()
    captured = capsys.readouterr()
    assert(captured.out == """[YESSS_AT]
YESSS_LOGIN = 06501234567
YESSS_PASSWD = mySecretPassword
# you can define a default recipient (will be overridden by -t option)
# YESSS_TO = +43664123123123
""")
