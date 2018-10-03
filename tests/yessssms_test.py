""" Mocked tests for YesssSMS Module """
import pytest
import requests
import requests_mock
import YesssSMS
from YesssSMS.const import VERSION

try:
    from secrets import YESSS_LOGIN, YESSS_PASSWD, YESSS_TO
except ImportError:
    YESSS_LOGIN = "06641234567"
    YESSS_PASSWD = "testpasswd"
    YESSS_TO = "06501234567"


def test_credentials_work():
    """test for working credentials"""
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
    """test if login works"""
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
    """test error handling for empty message"""
    sms = YesssSMS.YesssSMS()
    with pytest.raises(ValueError):
        sms.send(YESSS_TO, "")


def test_login_error():
    """test error handling of faulty login"""
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

def test_login_suspended_error():
    """test error handling for suspended account"""
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
    """test SMS sending"""
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
                          text="<h1>Ihre SMS wurde erfolgreich verschickt!</h1>"
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
