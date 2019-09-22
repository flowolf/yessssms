"""Live Tests for YesssSMS module."""
import time
import pytest
import requests
import YesssSMS

try:
    from secrets import YESSS_LOGIN, YESSS_PASSWD, YESSS_TO
except ImportError:
    raise ImportError("need login data for live testing!")


def test_credentials_exist():
    """Check for existing login data."""
    sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
    # pylint: disable=protected-access
    assert isinstance(sms._logindata["login_rufnummer"], str)
    # pylint: disable=protected-access
    assert isinstance(sms._logindata["login_passwort"], str)
    # pylint: disable=protected-access
    assert len(sms._logindata["login_rufnummer"]) > 10
    # pylint: disable=protected-access
    assert sms._logindata["login_passwort"]


def test_login():
    """Test if login works."""
    sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
    # pylint: disable=protected-access
    session, request = sms._login(requests.Session(), get_request=True)
    # pylint: disable=protected-access
    session.get(sms._logout_url)
    assert sms._logindata["login_rufnummer"][-7:] + "</a>" in request.text
    # pylint: disable=protected-access
    assert request.url == sms._kontomanager


def test_empty_message():
    """Test error handling for empty message."""
    sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
    with pytest.raises(ValueError):
        sms.send(YESSS_TO, "")


def test_login_error():
    """Test error handling of faulty login."""
    # non existing user and password
    sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
    # LoginError
    with pytest.raises(sms.LoginError):
        sms.send(YESSS_TO, "test")


def test_login_suspended_error():
    """Test error handling for suspended account."""
    # non existing user and password
    sms = YesssSMS.YesssSMS("0000000123", "CU4uNvCsee")
    assert sms.login_data_valid() is False
    time.sleep(1.4)
    assert sms.login_data_valid() is False
    time.sleep(2.6)
    assert sms.login_data_valid() is False
    time.sleep(3.1)
    # LoginError
    with pytest.raises(sms.AccountSuspendedError):
        sms.send(YESSS_TO, "test")
    assert sms.account_is_suspended() is True


def test_send_sms():
    """Test SMS sending."""
    try:
        sms = YesssSMS.YesssSMS(YESSS_LOGIN, YESSS_PASSWD)
        sms.send(
            YESSS_TO,
            "testing YesssSMS version {}, seems to work! :)".format(sms.version()),
        )
    except (ValueError, RuntimeError):
        pytest.fail("Exception raised while sending SMS")
