#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for YesssSMS Module."""
#
# pylint: disable-msg=C0103
import sys
from unittest import mock

import pytest
import requests

import requests_mock

import YesssSMS

from YesssSMS.CLI import CLI

from YesssSMS.const import PROVIDER_URLS

# import YesssSMS.const
from YesssSMS.const import (
    VERSION,
    _UNSUPPORTED_CHARS_STRING,
    CONFIG_FILE_CONTENT,
    CONFIG_FILE_PATHS,
)

# currently only testing yesss
PROVIDER = PROVIDER_URLS["yesss"]

_LOGIN_URL = PROVIDER["LOGIN_URL"]
_LOGOUT_URL = PROVIDER["LOGOUT_URL"]
_KONTOMANAGER_URL = PROVIDER["KONTOMANAGER_URL"]
_WEBSMS_URL = PROVIDER["WEBSMS_URL"]


try:
    from secrets import LOGIN, YESSS_PASSWD, YESSS_TO
except ImportError:
    LOGIN = "06641234567"
    YESSS_PASSWD = "testpasswd"
    YESSS_TO = "06501234567"


@pytest.fixture
def valid_connection():
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
def invalid_login(valid_connection):
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


def test_connection_error(connection_error):
    """Test connection error."""
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
    with pytest.raises(YesssSMS.YesssSMS.ConnectionError):
        sms.login_data_valid()


def test_login_url_getter():
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)

    login_url = sms.get_login_url()
    assert login_url == YesssSMS.const.PROVIDER_URLS["yesss"]["LOGIN_URL"]


def test_provider_getter():
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD, provider="goood")
    provider = sms.get_provider()

    # pylint: disable=protected-access
    assert provider == sms._provider


def test_credentials_work():
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


def test_login():
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


def test_empty_message(valid_connection):
    """Test error handling for empty message."""
    sms = YesssSMS.YesssSMS(LOGIN, YESSS_PASSWD)
    with pytest.raises(ValueError):
        sms.send(YESSS_TO, "")
    with pytest.raises(sms.EmptyMessageError):
        sms.send(YESSS_TO, "")


def test_login_error():
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


def test_login_empty_password_error():
    """Test error handling of empty password."""
    with pytest.raises(YesssSMS.YesssSMS.MissingLoginCredentialsError):
        _ = YesssSMS.YesssSMS("0000000000", None)


def test_login_empty_login_error(invalid_login):
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


def test_unsupported_chars_error():
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


def test_sms_sending_error():
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


def test_login_suspended_error():
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


def test_send_sms():
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


def test_cli_print_config_file(capsys):
    """test for correct config file output"""
    CLI.print_config_file()
    captured = capsys.readouterr()
    assert captured.out == CONFIG_FILE_CONTENT


def test_cli_version_info(capsys):
    """test for correct version info print"""
    CLI.version_info()
    captured = capsys.readouterr()
    assert captured.out == "yessssms " + VERSION + "\n"


def test_cli_boolean_args():
    """test parser for boolean arguments"""
    args = CLI.parse_args(["--version"])
    assert args.version is True

    args = CLI.parse_args(["--test"])
    assert args.test is True

    args = CLI.parse_args(["--print-config-file"])
    assert args.print_config_file is True

    args = CLI.parse_args(["-T"])
    assert args.check_login is True


def test_cli_argparse():
    """test parser for different arguments"""
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


def test_cli_with_test_args():
    """Test command line arguments with --test"""
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


def test_cli_with_printconfigfile_arg(capsys):
    """Test print-config-file parameter"""
    testargs = ["yessssms", "--print-config-file"]
    with mock.patch.object(sys, "argv", testargs):
        CLI()
        captured = capsys.readouterr()
        assert captured.out == CONFIG_FILE_CONTENT


def test_cli_with_version_arg(capsys):
    """Test version cli argument"""
    testargs = ["yessssms", "--version"]
    with mock.patch.object(sys, "argv", testargs):
        CLI()
        captured = capsys.readouterr()
        assert captured.out == "yessssms " + VERSION + "\n"


def test_cli_with_no_arg(capsys):
    """Test handling of no arguments"""
    testargs = ["yessssms"]
    with mock.patch.object(sys, "argv", testargs):
        CLI()
        captured = capsys.readouterr()
        assert "usage: yessssms " in captured.out


def test_cli_with_configfile_arg():
    """Test config-file argument"""
    testargs = [
        "yessssms",
        "-c",
        "/tmp/testconfig_1234.conf",
        "-m",
        "test",
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
            CLI()
            assert "/tmp/testconfig_1234.conf" in CONFIG_FILE_PATHS


def test_cli_with_test_login_arg(capsys):
    """Test check-login argument"""
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


def test_cli_with_invalid_test_login_arg(capsys):
    """Test check-login argument"""
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


@mock.patch("YesssSMS.const.CONFIG_FILE_PATHS", [])
def test_cli_with_no_login_or_password(capsys):
    """Test empty login parameters"""
    testargs = ["yessssms", "-m", "test"]
    print("test:..." + str(YesssSMS.const.CONFIG_FILE_PATHS))
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
            CLI()
            captured = capsys.readouterr()
            assert "error: no username or password defined " in captured.out


def test_cli_with_mvno_arg_error():
    """Test command line arguments with wrong --mvno"""
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
            CLI(test=True)


def test_cli_stdin():
    """Test command line with stdin"""
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

                message = CLI(test=True).message

    assert message.startswith(
        """Da steh’ ich nun, ich armer Thor!
Und bin so klug als wie zuvor;"""
    )
    assert message == in_message[:MAX_MESSAGE_LENGTH_STDIN]


def test_cli_with_mvno_educom_arg():
    """Test command line arguments with --mvno"""
    from YesssSMS.const import PROVIDER_URLS

    PROVIDER = PROVIDER_URLS["EDUCOM".lower()]

    _LOGIN_URL = PROVIDER["LOGIN_URL"]
    _LOGOUT_URL = PROVIDER["LOGOUT_URL"]
    _KONTOMANAGER_URL = PROVIDER["KONTOMANAGER_URL"]
    _WEBSMS_URL = PROVIDER["WEBSMS_URL"]

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
            sms = CLI(test=True).yessssms
            assert "educom" == sms._provider
            assert _LOGIN_URL == sms._login_url
            assert _LOGOUT_URL == sms._logout_url
            assert _KONTOMANAGER_URL == sms._kontomanager
            assert _WEBSMS_URL == sms._websms_url
            assert _LOGIN_URL == "https://educom.kontomanager.at/index.php"
            assert _LOGOUT_URL == "https://educom.kontomanager.at/index.php?dologout=2"
            assert _KONTOMANAGER_URL == "https://educom.kontomanager.at/kundendaten.php"
            assert _WEBSMS_URL == "https://educom.kontomanager.at/websms_send.php"


def test_cli_with_mvno_simfonie_arg():
    """Test command line arguments with --mvno"""
    from YesssSMS.const import PROVIDER_URLS

    PROVIDER = PROVIDER_URLS["SIMfonie".lower()]

    _LOGIN_URL = PROVIDER["LOGIN_URL"]
    _LOGOUT_URL = PROVIDER["LOGOUT_URL"]
    _KONTOMANAGER_URL = PROVIDER["KONTOMANAGER_URL"]
    _WEBSMS_URL = PROVIDER["WEBSMS_URL"]

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
            sms = CLI(test=True).yessssms
            assert "simfonie" == sms._provider
            assert _LOGIN_URL == sms._login_url
            assert _LOGOUT_URL == sms._logout_url
            assert _KONTOMANAGER_URL == sms._kontomanager
            assert _WEBSMS_URL == sms._websms_url
            assert _LOGIN_URL == "https://simfonie.kontomanager.at/index.php"
            assert (
                _LOGOUT_URL == "https://simfonie.kontomanager.at/index.php?dologout=2"
            )
            assert (
                _KONTOMANAGER_URL == "https://simfonie.kontomanager.at/kundendaten.php"
            )
            assert _WEBSMS_URL == "https://simfonie.kontomanager.at/websms_send.php"


def test_cli_with_mvno_div_arg():
    """Test command line arguments with --mvno"""
    from YesssSMS.const import PROVIDER_URLS

    all_providers = PROVIDER_URLS.keys()

    for provider in all_providers:

        PROVIDER = PROVIDER_URLS[provider.lower()]

        _LOGIN_URL = PROVIDER["LOGIN_URL"]
        _LOGOUT_URL = PROVIDER["LOGOUT_URL"]
        _KONTOMANAGER_URL = PROVIDER["KONTOMANAGER_URL"]
        _WEBSMS_URL = PROVIDER["WEBSMS_URL"]

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
                cli = CLI(test=True)
                sms = cli.yessssms
                assert provider == sms._provider
                assert _LOGIN_URL == sms._login_url
                assert _LOGOUT_URL == sms._logout_url
                assert _KONTOMANAGER_URL == sms._kontomanager
                assert _WEBSMS_URL == sms._websms_url


def test_default_config_file_paths():
    assert "~/.config/yessssms.conf" in CONFIG_FILE_PATHS
    assert "/etc/yessssms.conf" in CONFIG_FILE_PATHS
