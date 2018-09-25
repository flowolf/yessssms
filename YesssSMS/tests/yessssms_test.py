import pytest
import YesssSMS
from requests import Session

try:
    from secrets import *
except:
    pass

def test_credentials_exist():
    sms = YesssSMS.YesssSMS()
    assert type(sms._logindata['login_rufnummer']) == str
    assert type(sms._logindata['login_passwort']) == str
    assert len(sms._logindata['login_rufnummer']) > 10
    assert len(sms._logindata['login_passwort']) > 0

def test_login():
    sms = YesssSMS.YesssSMS()
    s,r = sms._login(Session(), get_request=True)
    s.get(sms._logout_url)
    assert sms._logindata['login_rufnummer'][-7:]+"</a>" in r.text
    assert r.url == sms._kontomanager

def test_empty_message():
    sms = YesssSMS.YesssSMS()
    with pytest.raises(ValueError) as e_info:
        sms.send(YESSS_TO, "")

def test_login_error():
    # non existing user and password
    sms = YesssSMS.YesssSMS("0000000000","2d4faa0ea6f55813")
    # LoginError
    with pytest.raises(ValueError) as e_info:
        sms.send(YESSS_TO, "test")

def test_send_sms():
    try:
        sms = YesssSMS.YesssSMS()
        sms.send(YESSS_TO, "testing YesssSMS version {}, seems to work! :)".format(sms._version))
    except ValueError or RuntimeError:
        pytest.fail("Exception raised while sending SMS")
