#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for YesssSMS Module."""
#
# pylint: disable-msg=C0103
import os
import sys
from unittest import mock

import YesssSMS
from YesssSMS.CLI import CLI
from YesssSMS.CLI import run as cli_run
from YesssSMS.const import (
    CONFIG_FILE_CONTENT,
    CONFIG_FILE_PATHS,
    PROVIDER_URLS,
    VERSION,
    _UNSUPPORTED_CHARS_STRING,
)


import pytest

import requests

import requests_mock


PROVIDER = PROVIDER_URLS["yesss"]

_LOGIN_URL = PROVIDER["LOGIN_URL"]
_LOGOUT_URL = PROVIDER["LOGOUT_URL"]
_KONTOMANAGER_URL = PROVIDER["KONTOMANAGER_URL"]
_WEBSMS_URL = PROVIDER["WEBSMS_URL"]

# make sure env is empty
os.environ = {}

LOGIN = "06641234567"
YESSS_PASSWD = "testpasswd"
YESSS_TO = "06501234567"


@pytest.fixture
def valid_connection():
    """Decorate connection to be valid."""
    sms = YesssSMS.YesssSMS("", "", provider="yesss")
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
            text="test..." + LOGIN + "</a>",
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._websms_url,
            status_code=200,
            text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        yield


@pytest.fixture
def valid_mock_connection():
    """Decorate connection to be mocked."""
    # sms = YesssSMS.YesssSMS("", "", provider="yesss")
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            "mock://kontomanager.at/index.php",
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": "mock://kontomanager.at/kundendaten.php"},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            "mock://kontomanager.at/kundendaten.php",
            status_code=200,
            text="test..." + LOGIN + "</a>",
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            "mock://kontomanager.at/websms_send.php",
            status_code=200,
            text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            "mock://kontomanager.at/index.php?dologout=2",
            status_code=200,
        )
        yield


@pytest.fixture
def valid_goood_mock_connection():
    """Decorate connection to be mocked and working."""
    # sms = YesssSMS.YesssSMS("", "", provider="yesss")
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            "https://goood.kontomanager.at/index.php",
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": "https://goood.kontomanager.at/kundendaten.php"},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            "https://goood.kontomanager.at/kundendaten.php",
            status_code=200,
            text="test..." + LOGIN + "</a>",
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            "https://goood.kontomanager.at/websms_send.php",
            status_code=200,
            text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            "https://goood.kontomanager.at/index.php?dologout=2",
            status_code=200,
        )
        yield


@pytest.fixture
def valid_wowww_mock_connection():
    """Decorate connection to be mocked and working."""
    # sms = YesssSMS.YesssSMS("", "", provider="yesss")
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            "https://wowww.kontomanager.at/index.php",
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": "https://wowww.kontomanager.at/kundendaten.php"},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            "https://wowww.kontomanager.at/kundendaten.php",
            status_code=200,
            text="test..." + LOGIN + "</a>",
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            "https://wowww.kontomanager.at/websms_send.php",
            status_code=200,
            text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            "https://wowww.kontomanager.at/index.php?dologout=2",
            status_code=200,
        )
        yield


@pytest.fixture
def invalid_login(valid_connection):
    """Decorate connection to be mocked and invalid."""
    # sms = YesssSMS.YesssSMS("", "")
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            _LOGIN_URL,
            status_code=200,
            text="Bla bla<strong>Login nicht erfolgreichBlaBla",
        )
        yield


@pytest.fixture(name="connection_error")
def simulate_connection_error(valid_connection):
    """Simulate a connection error with requests."""
    path = "YesssSMS.YesssSMS._login"
    with mock.patch(path, side_effect=requests.exceptions.ConnectionError()):
        yield


@pytest.fixture(name="suspended_error")
def simulate_suspended_error(valid_connection):
    """Simulate a suspended error."""
    path = "YesssSMS.YesssSMS._login"
    with mock.patch(path, side_effect=YesssSMS.YesssSMS.AccountSuspendedError()):
        yield


@pytest.fixture(name="sending_error")
def simulate_sending_error(valid_connection):
    """Simulate a sending error."""
    path = "YesssSMS.YesssSMS.send"
    with mock.patch(path, side_effect=YesssSMS.YesssSMS.SMSSendingError()):
        yield


@pytest.fixture(name="unsupported_chars_error")
def simulate_unsupported_chars_error(valid_connection):
    """Simulate a sending error."""
    path = "YesssSMS.YesssSMS.send"
    with mock.patch(path, side_effect=YesssSMS.YesssSMS.UnsupportedCharsError()):
        yield


@pytest.fixture(name="empty_message_error")
def simulate_empty_message_error(valid_connection):
    """Simulate a empty_message error."""
    path = "YesssSMS.YesssSMS.send"
    with mock.patch(path, side_effect=YesssSMS.YesssSMS.EmptyMessageError):
        yield


@pytest.fixture
def mocked_config_file_custom_provider():
    """Mock config file with custom data."""
    data = """[YESSSSMS]
LOGIN =  06501234567
PASSWD = MySecre3tPassw0rd
DEFAULT_TO = +43664123123123
# MVNO = FANTASYMOBILE
[YESSSSMS_PROVIDER_URLS]
LOGIN_URL = mock://kontomanager.at/index.php
LOGOUT_URL = mock://kontomanager.at/index.php?dologout=2
KONTOMANAGER_URL = mock://kontomanager.at/kundendaten.php
WEBSMS_URL = mock://kontomanager.at/websms_send.php
"""
    with mock.patch(
        "configparser.open",
        # "builtins.open",
        mock.mock_open(read_data=data),
    ):
        yield


@pytest.fixture
def mocked_config_file_error():
    """Mock config file with erroneous data."""
    data = """
LOGIN =  06501234567
PASSWD = MySecre3tPassw0rd
"""
    with mock.patch(
        "configparser.open",
        # "builtins.open",
        mock.mock_open(read_data=data),
    ):
        yield


@pytest.fixture
def mocked_config_file():
    """Mock config file with data."""
    data = """[YESSSSMS]
LOGIN =  03211234567
PASSWD = MySecr3t
DEFAULT_TO = +43664123123123
MVNO = GOOOD
"""
    with mock.patch(
        "configparser.open",
        # "builtins.open",
        mock.mock_open(read_data=data),
    ):
        yield


@pytest.fixture
def config():
    """Mock config file with data."""
    data = """[YESSSSMS]
LOGIN =  03211234567
PASSWD = MySecr3t
DEFAULT_TO = +43664123123123
MVNO = YESSS
"""
    with mock.patch(
        "configparser.open",
        # "builtins.open",
        mock.mock_open(read_data=data),
    ):
        yield


@pytest.fixture
def environment_vars_set():
    """Mock env vars YESSSSMS_LOGIN and YESSSSMS_PASSWD."""
    os.environ["YESSSSMS_LOGIN"] = "03211234567"
    os.environ["YESSSSMS_PASSWD"] = "MySecr3t"
    os.environ["YESSSSMS_PROVIDER"] = "goood"
    os.environ["YESSSSMS_RECIPIENT"] = "066356789789"


@pytest.fixture
def environment_vars_set_wowww():
    """Mock env vars YESSSSMS_LOGIN and YESSSSMS_PASSWD."""
    os.environ["YESSSSMS_LOGIN"] = "03211234567"
    os.environ["YESSSSMS_PASSWD"] = "MySecr3t"
    os.environ["YESSSSMS_PROVIDER"] = "wowww"
    os.environ["YESSSSMS_RECIPIENT"] = "066356789780"


@mock.patch("YesssSMS.CLI.CONFIG_FILE_PATHS", ["testconfigfile.conf"])
@pytest.fixture(name="config_file")
def mocked_read_config():
    """Mock config file read."""
    # login, passwd, DEFAULT_RECIPIENT, PROVIDER, CUSTOM_PROVIDER_URLS
    data = ("03141592653", "MySecr3t", None, "yesss", None)
    with mock.patch("YesssSMS.CLI.CLI.read_config_files", return_value=data):
        yield


def test_cli_mocked_config_file(
    valid_mock_connection, mocked_config_file_custom_provider
):
    """Test CLI config file."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
    with mock.patch.object(sys, "argv", testargs):
        cli = CLI()
        print(cli.config_files)
        assert cli.yessssms._logindata["login_rufnummer"] == "06501234567"
        assert cli.yessssms._logindata["login_passwort"] == "MySecre3tPassw0rd"
        assert cli.yessssms._login_url == "mock://kontomanager.at/index.php"
        assert cli.yessssms._logout_url == "mock://kontomanager.at/index.php?dologout=2"
        assert cli.yessssms._kontomanager == "mock://kontomanager.at/kundendaten.php"
        assert cli.yessssms._websms_url == "mock://kontomanager.at/websms_send.php"

        assert cli.recipient == "+43664123123123"
        assert cli.message == "Bilde mir nicht ein was rechts zu wissen"


def test_goood_cli_mocked_config_file(valid_goood_mock_connection, mocked_config_file):
    """Test CLI config file."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
    with mock.patch.object(sys, "argv", testargs):
        cli = CLI()
        print(cli.config_files)
        assert cli.yessssms._logindata["login_rufnummer"] == "03211234567"
        assert cli.yessssms._logindata["login_passwort"] == "MySecr3t"
        assert cli.yessssms._provider == "goood"
        assert cli.yessssms._login_url == "https://goood.kontomanager.at/index.php"
        assert (
            cli.yessssms._logout_url
            == "https://goood.kontomanager.at/index.php?dologout=2"
        )
        assert (
            cli.yessssms._kontomanager
            == "https://goood.kontomanager.at/kundendaten.php"
        )
        assert (
            cli.yessssms._websms_url == "https://goood.kontomanager.at/websms_send.php"
        )

        assert cli.recipient == "+43664123123123"
        assert cli.message == "Bilde mir nicht ein was rechts zu wissen"


def test_cli_mocked_config_file_error(
    valid_mock_connection, mocked_config_file_error, capsys
):
    """Test CLI config file error."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = [
        "yessssms",
        "-m",
        "Bilde mir nicht ein was rechts zu wissen",
        "-c",
        "/tmp/custom_settings.conf",
    ]
    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert "error: missing settings or invalid settings." in capsys.readouterr().out
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 8
    assert "/tmp/custom_settings.conf" in CONFIG_FILE_PATHS


def test_cli_suspended_error(
    valid_mock_connection, mocked_config_file_custom_provider, suspended_error, capsys
):
    """Test CLI suspended error."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 4
    assert (
        "error: your account was suspended because of 3 failed login attempts."
        in capsys.readouterr().out
    )


def test_cli_sending_error(
    valid_mock_connection, mocked_config_file_custom_provider, sending_error, capsys
):
    """Test CLI SMS sending error."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 5
    assert "error: could not send SMS" in capsys.readouterr().out


def test_cli_unsupported_chars_error(
    valid_mock_connection,
    mocked_config_file_custom_provider,
    unsupported_chars_error,
    capsys,
):
    """Test CLI unsupported chars error."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 6
    assert "error: message contains unsupported character(s)" in capsys.readouterr().out


def test_cli_empty_message_error(
    valid_mock_connection,
    mocked_config_file_custom_provider,
    empty_message_error,
    capsys,
):
    """Test CLI empty_message error."""
    if int(sys.version[2]) < 7:  # don't run test on 3.5, 3.6
        pytest.skip("issue with mock_open")

    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 7
    assert "error: cannot send empty message" in capsys.readouterr().out


def test_connection_error(config, connection_error):
    """Test connection error."""
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
    with pytest.raises(YesssSMS.YesssSMS.ConnectionError):
        sms.login_data_valid()


def test_cli_config_file(valid_connection, config_file):
    """Test CLI config file."""
    testargs = ["yessssms", "-m", "Blablabla", "-t", "03141512345"]
    with mock.patch.object(sys, "argv", testargs):
        cli = CLI()
        assert cli.message == "Blablabla"
        assert cli.recipient == "03141512345"
        assert cli.yessssms._logindata["login_rufnummer"] == "03141592653"
        assert cli.yessssms._logindata["login_passwort"] == "MySecr3t"
        assert cli.yessssms._provider == "yesss"


def test_cli_connection_error(config, connection_error, capsys):
    """Test connection error."""
    testargs = [
        "yessssms",
        "--test",
        "-l",
        "06641234567",
        "-p",
        "passw0rd",
        "-t",
        "+43676564736",
    ]
    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 3
    assert "error: could not connect to provider. " in capsys.readouterr().out


def test_login_url_getter(config,):
    """Test login url getter."""
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)

    login_url = sms.get_login_url()
    assert login_url == YesssSMS.const.PROVIDER_URLS["yesss"]["LOGIN_URL"]


def test_provider_getter(config,):
    """Test provider getter."""
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD, provider="goood")
    provider = sms.get_provider()

    # pylint: disable=protected-access
    assert provider == sms._provider


def test_credentials_work(config,):
    """Test for working credentials."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            _LOGIN_URL,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        assert sms.version() == VERSION
        print(
            "user: {}, pass: {}, to: {}".format(
                LOGIN, YESSS_PASSWD[0] + (len(YESSS_PASSWD) - 1) * "*", YESSS_TO
            )
        )
        assert sms.login_data_valid() is True
        # pylint: disable=protected-access
        assert isinstance(sms._logindata["login_rufnummer"], str)
        # pylint: disable=protected-access
        assert isinstance(sms._logindata["login_passwort"], str)
        # pylint: disable=protected-access
        assert len(sms._logindata["login_rufnummer"]) > 10
        # pylint: disable=protected-access
        assert sms._logindata["login_passwort"]


def test_login(config,):
    """Test if login works."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
            text="test..." + LOGIN + "</a>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        # pylint: disable=protected-access
        session, request = sms._login(requests.Session(), get_request=True)
        # pylint: disable=protected-access
        session.get(sms._logout_url)
        # pylint: disable=protected-access
        assert sms._logindata["login_rufnummer"][-7:] + "</a>" in request.text
        # pylint: disable=protected-access
        assert request.url == sms._kontomanager


def test_empty_message(config, valid_connection):
    """Test error handling for empty message."""
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
    with pytest.raises(ValueError):
        sms.send(YESSS_TO, "")
    with pytest.raises(sms.EmptyMessageError):
        sms.send(YESSS_TO, "")


def test_login_error(config,):
    """Test error handling of faulty login."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=200,
            text="<strong>Login nicht erfolgreich",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        with pytest.raises(sms.LoginError):
            sms.send(YESSS_TO, "test")


def test_login_empty_password_error(config,):
    """Test error handling of empty password."""
    with pytest.raises(YesssSMS.YesssSMS.MissingLoginCredentialsError):
        _ = YesssSMS.YesssSMS("0000000000", None)


def test_login_empty_login_error(invalid_login):  # xxxxxx
    """Test error handling of empty login."""
    sms = YesssSMS.YesssSMS("", "2d4faa0ea6f55813")
    with pytest.raises(sms.LoginError):
        sms.send(YESSS_TO, "test")


def test_no_recipient_error(config,):
    """Test error handling of no recipient."""
    sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
    with pytest.raises(sms.NoRecipientError):
        sms.send("", "test")


def test_recipient_not_str_error(config,):
    """Test error handling of wrong recipient data type."""
    sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
    with pytest.raises(ValueError):
        sms.send(176264916361239, "test")


def test_message_sending_error(config,):
    """Test handling of status codes other than 200 and 302."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._websms_url,
            status_code=400,
            text="<h1>OOOOPS</h1>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        with pytest.raises(sms.SMSSendingError):
            sms.send(YESSS_TO, "test")


def test_unsupported_chars_error(config,):
    """Test error handling for unsupported chars."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._websms_url,
            status_code=200,
            text=_UNSUPPORTED_CHARS_STRING,
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        with pytest.raises(sms.UnsupportedCharsError):
            sms.send(YESSS_TO, "test")


def test_sms_sending_error(config,):
    """Test error handling for missing success string."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS("0000000000", "2d4faa0ea6f55813")
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._websms_url,
            status_code=200,
            text="some text i'm not looking for",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        with pytest.raises(sms.SMSSendingError):
            sms.send(YESSS_TO, "test")


def test_login_suspended_error(config,):
    """Test error handling for suspended account."""
    with requests_mock.Mocker() as m:
        # non existing user and password
        sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=200,
            text="<strong>Login nicht erfolgreich bla Wegen "
            "3 ungültigen Login-Versuchen ist Ihr Account "
            "für eine Stunde gesperrt.",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )

        assert sms.login_data_valid() is False
        # LoginError
        with pytest.raises(sms.AccountSuspendedError):
            sms.send(YESSS_TO, "test")
        assert sms.account_is_suspended() is True


def test_send_sms(config,):
    """Test SMS sending."""
    with requests_mock.Mocker() as m:
        sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._login_url,
            status_code=302,
            # pylint: disable=protected-access
            headers={"location": sms._kontomanager},
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._kontomanager,
            status_code=200,
        )
        m.register_uri(
            "POST",
            # pylint: disable=protected-access
            sms._websms_url,
            status_code=200,
            text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
        )
        m.register_uri(
            "GET",
            # pylint: disable=protected-access
            sms._logout_url,
            status_code=200,
        )
        try:
            sms.send(
                YESSS_TO,
                "testing YesssSMS version {}, seems to work! :)".format(sms.version()),
            )
        except (ValueError, RuntimeError):
            pytest.fail("Exception raised while sending SMS")


def test_cli_print_config_file(config, capsys):
    """Test for correct config file output."""
    CLI.print_config_file()
    captured = capsys.readouterr()
    assert captured.out == CONFIG_FILE_CONTENT


def test_cli_version_info(config, capsys):
    """Test for correct version info print."""
    CLI.version_info()
    captured = capsys.readouterr()
    assert captured.out == "yessssms " + VERSION + "\n"


def test_cli_boolean_args(config,):
    """Test parser for boolean arguments."""
    args = CLI.parse_args(["--version"])
    assert args.version is True

    args = CLI.parse_args(["--test"])
    assert args.test is True

    args = CLI.parse_args(["--print-config-file"])
    assert args.print_config_file is True

    args = CLI.parse_args(["-T"])
    assert args.check_login is True


def test_cli_argparse(config,):
    """Test parser for different arguments."""
    args = CLI.parse_args(["-t", "0664123456"])
    assert args.recipient == "0664123456"

    args = CLI.parse_args(["--to", "0664123456"])
    assert args.recipient == "0664123456"

    args = CLI.parse_args(["-l", "0676456789123"])
    assert args.login == "0676456789123"

    args = CLI.parse_args(["--login", "0676456789123"])
    assert args.login == "0676456789123"

    args = CLI.parse_args(["-p", "s3cret..11"])
    assert args.password == "s3cret..11"

    args = CLI.parse_args(["--password", "s3cret..11"])
    assert args.password == "s3cret..11"

    args = CLI.parse_args(["-c", ".yessssms.config"])
    assert args.configfile == ".yessssms.config"

    args = CLI.parse_args(["--configfile", ".yessssms.config"])
    assert args.configfile == ".yessssms.config"

    args = CLI.parse_args(["--message", "testmessage 123 - can you see this?"])
    assert args.message == "testmessage 123 - can you see this?"

    args = CLI.parse_args(["-m", "testmessage 123 - can you see this?"])
    assert args.message == "testmessage 123 - can you see this?"

    args = CLI.parse_args(["--mvno", "YESSS"])
    assert args.provider == "YESSS"

    args = CLI.parse_args(["--mvno", "EDUCOM"])
    assert args.provider == "EDUCOM"

    args = CLI.parse_args(["--mvno", "SIMfonie"])
    assert args.provider == "SIMfonie"

    args = CLI.parse_args(["--mvno", "BLABLABLA"])
    assert args.provider == "BLABLABLA"


def test_cli_with_test_args(config,):
    """Test command line arguments with --test."""
    testargs = [
        "yessssms",
        "--test",
        "-l",
        "06641234567",
        "-p",
        "passw0rd",
        "-t",
        "+43676564736",
    ]
    with mock.patch.object(sys, "argv", testargs):
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                _LOGIN_URL,
                status_code=302,
                # pylint: disable=protected-access
                headers={"location": _KONTOMANAGER_URL},
            )
            m.register_uri("GET", _KONTOMANAGER_URL, status_code=200)
            m.register_uri(
                "POST",
                _WEBSMS_URL,
                status_code=200,
                text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
            )
            m.register_uri("GET", _LOGOUT_URL, status_code=200)
            val = CLI().exit_status
            assert val == 0


def test_cli_with_printconfigfile_arg(config, capsys):
    """Test print-config-file parameter."""
    testargs = ["yessssms", "--print-config-file"]
    with mock.patch.object(sys, "argv", testargs):
        CLI()
        captured = capsys.readouterr()
        assert captured.out == CONFIG_FILE_CONTENT


def test_cli_with_version_arg(config, capsys):
    """Test version cli argument."""
    testargs = ["yessssms", "--version"]
    with mock.patch.object(sys, "argv", testargs):
        CLI()
        captured = capsys.readouterr()
        assert captured.out == "yessssms " + VERSION + "\n"


def test_cli_with_no_arg(config, capsys):
    """Test handling of no arguments."""
    testargs = ["yessssms"]
    with mock.patch.object(sys, "argv", testargs):
        CLI()
        captured = capsys.readouterr()
        assert "usage: yessssms " in captured.out


def test_cli_with_test_login_arg(config, capsys):
    """Test check-login argument."""
    testargs = ["yessssms", "-m", "test", "-l", "06641234567", "-p", "passw0rd", "-T"]
    with mock.patch.object(sys, "argv", testargs):
        with requests_mock.Mocker() as m:

            m.register_uri(
                "POST",
                # pylint: disable=protected-access
                _LOGIN_URL,
                status_code=302,
                # pylint: disable=protected-access
                headers={"location": _KONTOMANAGER_URL},
            )
            m.register_uri(
                "GET",
                # pylint: disable=protected-access
                _KONTOMANAGER_URL,
                status_code=200,
            )
            m.register_uri(
                "POST",
                # pylint: disable=protected-access
                _WEBSMS_URL,
                status_code=200,
                text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
            )
            m.register_uri(
                "GET",
                # pylint: disable=protected-access
                _LOGOUT_URL,
                status_code=200,
            )
            val = CLI().exit_status
            captured = capsys.readouterr()

            assert val == 0
            assert captured.out == "ok: login data is valid.\n"


def test_cli_with_invalid_test_login_arg(config, capsys):
    """Test check-login argument."""
    testargs = ["yessssms", "-m", "test", "-l", "06641234567", "-p", "passw0rd", "-T"]
    with mock.patch.object(sys, "argv", testargs):
        with requests_mock.Mocker() as m:

            m.register_uri(
                "POST",
                # pylint: disable=protected-access
                _LOGIN_URL,
                status_code=200,
                text="Bla bla<strong>Login nicht erfolgreichBlaBla",
            )
            m.register_uri(
                "GET",
                # pylint: disable=protected-access
                _LOGOUT_URL,
                status_code=200,
            )
            val = CLI().exit_status
            captured = capsys.readouterr()

            assert val == 1
            assert "error: login data is NOT valid" in captured.out


@mock.patch("YesssSMS.CLI.CONFIG_FILE_PATHS", [])
def test_cli_with_no_login_or_password(config, capsys, valid_connection):
    """Test empty login parameters."""
    testargs = ["yessssms", "-m", "test"]  # "-l", "\"\"", "-p", "\"\""]
    # print("test:..." + str(YesssSMS.const.CONFIG_FILE_PATHS))
    with (mock.patch.object(sys, "argv", testargs)):
        with pytest.raises(SystemExit) as wrapped_e:
            CLI()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 2
    captured = capsys.readouterr()
    assert "error: no username or password defined " in captured.out


def test_cli_with_mvno_arg_error(config,):
    """Test command line arguments with wrong --mvno."""
    from YesssSMS.YesssSMS import YesssSMS

    testargs = [
        "yessssms",
        "--test",
        "-l",
        "06641234567",
        "-p",
        "passw0rd",
        "-t",
        "+43676564736",
        "--mvno",
        "UNKNOWN_provider",
    ]

    with mock.patch.object(sys, "argv", testargs):
        with pytest.raises(YesssSMS.UnsupportedProviderError):
            cli_run()


def test_cli_stdin(config,):
    """Test command line with stdin."""
    from YesssSMS.YesssSMS import MAX_MESSAGE_LENGTH_STDIN

    testargs = ["yessssms", "--test", "-l", "06641234567", "-p", "passw0rd", "-m", "-"]

    in_message = """Da steh’ ich nun, ich armer Thor!
Und bin so klug als wie zuvor;
Heiße Magister, heiße Doctor gar,
Und ziehe schon an die zehen Jahr,
Herauf, herab und quer und krumm,
Meine Schüler an der Nase herum –
Und sehe, daß wir nichts wissen können!
Das will mir schier das Herz verbrennen.
Zwar bin ich gescheidter als alle die Laffen,
Doctoren, Magister, Schreiber und Pfaffen;
Mich plagen keine Scrupel noch Zweifel,
Fürchte mich weder vor Hölle noch Teufel –
Dafür ist mir auch alle Freud’ entrissen,
Bilde mir nicht ein was rechts zu wissen,
Bilde mir nicht ein, ich könnte was lehren,
Die Menschen zu bessern und zu bekehren.
Auch hab’ ich weder Gut noch Geld,
Noch Ehr’ und Herrlichkeit der Welt.
Es möchte kein Hund so länger leben!
Drum hab’ ich mich der Magie ergeben,
Ob mir durch Geistes Kraft und Mund
Nicht manch Geheimniß würde kund;
Daß ich nicht mehr mit sauerm Schweiß,
Zu sagen brauche, was ich nicht weiß;"""
    with mock.patch.object(sys, "argv", testargs):
        with mock.patch.object(sys, "stdin", in_message):
            with requests_mock.Mocker() as m:
                m.register_uri(
                    "POST",
                    # pylint: disable=protected-access
                    _LOGIN_URL,
                    status_code=302,
                    # pylint: disable=protected-access
                    headers={"location": _KONTOMANAGER_URL},
                )
                m.register_uri(
                    "GET",
                    # pylint: disable=protected-access
                    _KONTOMANAGER_URL,
                    status_code=200,
                )
                m.register_uri(
                    "POST",
                    # pylint: disable=protected-access
                    _WEBSMS_URL,
                    status_code=200,
                    text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
                )
                m.register_uri(
                    "GET",
                    # pylint: disable=protected-access
                    _LOGOUT_URL,
                    status_code=200,
                )

                message = CLI().message

    assert message.startswith(
        """Da steh’ ich nun, ich armer Thor!
Und bin so klug als wie zuvor;"""
    )
    assert message == in_message[:MAX_MESSAGE_LENGTH_STDIN]


def test_cli_with_mvno_educom_arg(config,):
    """Test command line arguments with --mvno."""
    from YesssSMS.const import PROVIDER_URLS

    provider = PROVIDER_URLS["EDUCOM".lower()]

    login_url = provider["LOGIN_URL"]
    logout_url = provider["LOGOUT_URL"]
    kontomanager_url = provider["KONTOMANAGER_URL"]
    websms_url = provider["WEBSMS_URL"]

    testargs = [
        "yessssms",
        "--test",
        "-l",
        "06641234567",
        "-p",
        "passw0rd",
        "-t",
        "+43676564736",
        "--mvno",
        "EDUCOM",
    ]
    with mock.patch.object(sys, "argv", testargs):
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                login_url,
                status_code=302,
                # pylint: disable=protected-access
                headers={"location": kontomanager_url},
            )
            m.register_uri("GET", kontomanager_url, status_code=200)
            m.register_uri(
                "POST",
                websms_url,
                status_code=200,
                text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
            )
            m.register_uri("GET", logout_url, status_code=200)
            sms = CLI().yessssms
            assert "educom" == sms._provider
            assert login_url == sms._login_url
            assert logout_url == sms._logout_url
            assert kontomanager_url == sms._kontomanager
            assert websms_url == sms._websms_url
            assert login_url == "https://educom.kontomanager.at/index.php"
            assert logout_url == "https://educom.kontomanager.at/index.php?dologout=2"
            assert kontomanager_url == "https://educom.kontomanager.at/kundendaten.php"
            assert websms_url == "https://educom.kontomanager.at/websms_send.php"


def test_cli_with_mvno_simfonie_arg(config,):
    """Test command line arguments with --mvno."""
    from YesssSMS.const import PROVIDER_URLS

    provider = PROVIDER_URLS["SIMfonie".lower()]

    login_url = provider["LOGIN_URL"]
    logout_url = provider["LOGOUT_URL"]
    kontomanager_url = provider["KONTOMANAGER_URL"]
    websms_url = provider["WEBSMS_URL"]

    testargs = [
        "yessssms",
        "--test",
        "-l",
        "06641234567",
        "-p",
        "passw0rd",
        "-t",
        "+43676564736",
        "--mvno",
        "SIMfonie",
    ]
    with mock.patch.object(sys, "argv", testargs):
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                login_url,
                status_code=302,
                # pylint: disable=protected-access
                headers={"location": kontomanager_url},
            )
            m.register_uri("GET", kontomanager_url, status_code=200)
            m.register_uri(
                "POST",
                websms_url,
                status_code=200,
                text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
            )
            m.register_uri("GET", logout_url, status_code=200)
            sms = CLI().yessssms
            assert "simfonie" == sms._provider
            assert login_url == sms._login_url
            assert logout_url == sms._logout_url
            assert kontomanager_url == sms._kontomanager
            assert websms_url == sms._websms_url
            assert login_url == "https://simfonie.kontomanager.at/index.php"
            assert logout_url == "https://simfonie.kontomanager.at/index.php?dologout=2"
            assert (
                kontomanager_url == "https://simfonie.kontomanager.at/kundendaten.php"
            )
            assert websms_url == "https://simfonie.kontomanager.at/websms_send.php"


def test_cli_with_mvno_div_arg(config,):
    """Test command line arguments with --mvno."""
    from YesssSMS.const import PROVIDER_URLS

    all_providers = PROVIDER_URLS.keys()

    for provider in all_providers:

        current_provider = PROVIDER_URLS[provider.lower()]

        login_url = current_provider["LOGIN_URL"]
        logout_url = current_provider["LOGOUT_URL"]
        kontomanager_url = current_provider["KONTOMANAGER_URL"]
        websms_url = current_provider["WEBSMS_URL"]

        testargs = [
            "yessssms",
            "--test",
            "-l",
            "06641234567",
            "-p",
            "passw0rd",
            "-t",
            "+43676564736",
            "--mvno",
            provider.upper(),
        ]
        with mock.patch.object(sys, "argv", testargs):
            with requests_mock.Mocker() as m:
                m.register_uri(
                    "POST",
                    login_url,
                    status_code=302,
                    # pylint: disable=protected-access
                    headers={"location": kontomanager_url},
                )
                m.register_uri("GET", kontomanager_url, status_code=200)
                m.register_uri(
                    "POST",
                    websms_url,
                    status_code=200,
                    text="<h1>Ihre SMS wurde erfolgreich " + "verschickt!</h1>",
                )
                m.register_uri("GET", logout_url, status_code=200)
                cli = CLI()
                sms = cli.yessssms
                assert provider == sms._provider
                assert login_url == sms._login_url
                assert logout_url == sms._logout_url
                assert kontomanager_url == sms._kontomanager
                assert websms_url == sms._websms_url


def test_default_config_file_paths(config,):
    """Test default config file paths."""
    assert "~/.config/yessssms.conf" in CONFIG_FILE_PATHS
    assert "/etc/yessssms.conf" in CONFIG_FILE_PATHS


def test_custom_provider_setting(config,):
    """Test custom provider setting."""
    sms = YesssSMS.YesssSMS(
        LOGIN,
        YESSS_PASSWD,
        custom_provider={
            "LOGIN_URL": "https://example.com/login",
            "LOGOUT_URL": "https://example.com/logout",
            "KONTOMANAGER_URL": "https://example.com/kontomanager",
            "WEBSMS_URL": "https://example.com/websms",
        },
    )
    assert sms._login_url == "https://example.com/login"
    assert sms._logout_url == "https://example.com/logout"
    assert sms._kontomanager == "https://example.com/kontomanager"
    assert sms._websms_url == "https://example.com/websms"


def test_env_var_settings_set(config, environment_vars_set_wowww):
    """Test setting of environment variables in YesssSMS class."""
    sms = YesssSMS.YesssSMS()
    assert sms._logindata["login_rufnummer"] == "03211234567"
    assert sms._logindata["login_passwort"] == "MySecr3t"
    assert sms._provider == "wowww"

    os.environ["YESSSSMS_PROVIDER"] = "goood"
    sms = YesssSMS.YesssSMS("123456", "password")
    assert sms._logindata["login_rufnummer"] == "03211234567"
    assert sms._logindata["login_passwort"] == "MySecr3t"
    assert sms._provider == "goood"

    del os.environ["YESSSSMS_PROVIDER"]
    sms = YesssSMS.YesssSMS("123456")
    assert sms._logindata["login_rufnummer"] == "03211234567"
    assert sms._logindata["login_passwort"] == "MySecr3t"
    assert sms._provider == "yesss"

    del os.environ["YESSSSMS_LOGIN"]
    sms = YesssSMS.YesssSMS("123456", "password")
    assert sms._logindata["login_rufnummer"] == "123456"
    assert sms._logindata["login_passwort"] == "password"
    assert sms._provider == "yesss"


def test_read_no_env_config():
    """Test setting of environment variables in CLI."""
    data = ""
    with mock.patch(
        "configparser.open",
        # "builtins.open",
        mock.mock_open(read_data=data),
    ):
        testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]
        with (mock.patch.object(sys, "argv", testargs)):
            with pytest.raises(SystemExit) as wrapped_e:
                cli = CLI()
                assert cli.read_env_config() is None
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 2


def test_read_env_config1(valid_wowww_mock_connection, environment_vars_set_wowww):
    """Test setting of environment variables in CLI."""
    testargs = ["yessssms", "-m", "Bilde mir nicht ein was rechts zu wissen"]

    with (mock.patch.object(sys, "argv", testargs)):
        cli = CLI()
        (login, passwd, rec, prov, custom_urls) = cli.read_env_config()
        assert login == "03211234567"
        assert passwd == "MySecr3t"
        assert rec == "066356789780"
        assert prov == "wowww"
        assert custom_urls is None


def test_read_env_config2(config, environment_vars_set_wowww):
    """Test setting of environment variables in CLI."""
    sms = YesssSMS.YesssSMS()
    assert sms._provider == "wowww"


def test_read_env_config3(config, environment_vars_set):
    """Test setting of environment variables in CLI."""
    os.environ["YESSSSMS_PROVIDER"] = "goood"
    sms = YesssSMS.YesssSMS()
    assert sms._provider == "goood"


def test_read_env_config4(config, environment_vars_set):
    """Test setting of environment variables in CLI."""
    del os.environ["YESSSSMS_PROVIDER"]
    sms = YesssSMS.YesssSMS()
    assert sms._provider == "yesss"
