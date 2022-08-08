"""constants for YesssSMS."""
import json
import os

VERSION = ""
with open(
    os.path.dirname(os.path.realpath(__file__)) + "/version.json", encoding="utf-8"
) as f:
    VERSION = json.loads(f.read())["version"]
_UNSUPPORTED_CHARS_STRING = "<strong>Achtung:</strong> Ihre SMS konnte nicht \
versendet werden, da sie folgende ungültige Zeichen enthält:"
_LOGIN_ERROR_STRING = "<strong>Login nicht erfolgreich"
_LOGIN_LOCKED_MESS = "Wegen 3 ungültigen Login-Versuchen ist Ihr Account für \
eine Stunde gesperrt."
_LOGIN_LOCKED_MESS_ENG = "because of 3 failed login-attempts, your account \
has been suspended for one hour"
_UNSUPPORTED_CHARS_STRING = "<strong>Achtung:</strong> Ihre SMS konnte nicht \
versendet werden, da sie folgende ungültige Zeichen enthält:"
_SMS_SENDING_SUCCESSFUL_STRING = ">Ihre SMS wurde erfolgreich verschickt!<"

_SMS_FORM_ID = "smsform"
_SMS_FORM_ID_VALUE = "value"

PROVIDER_TLDS = {
    "billitel": "billitel.kontomanager.at",
    "fenercell": "fenercell.kontomanager.at",
    "educom": "educom.kontomanager.at",
    "goood": "goood.kontomanager.at",
    "kronemobile": "kronemobile.kontomanager.at",
    "georg": "kundencenter.georg.at",
    "kuriermobil": "kuriermobil.kontomanager.at",
    "simfonie": "simfonie.kontomanager.at",
    "teleplanet": "teleplanet.kontomanager.at",
    "wowww": "wowww.kontomanager.at",
    "yooopi": "yooopi.kontomanager.at",
}

PROVIDER_URLS = {
    "yesss": {
        "LOGIN_URL": "https://www.yesss.at/kontomanager.at/index.php",
        "LOGOUT_URL": "https://www.yesss.at/kontomanager.at/index.php?dologout=2",
        "KONTOMANAGER_URL": "https://www.yesss.at/kontomanager.at/kundendaten.php",
        "WEBSMS_FORM_URL": "https://www.yesss.at/kontomanager.at/websms.php",
        "SEND_SMS_URL": "https://www.yesss.at/kontomanager.at/websms_send.php",
    },
    "billitel": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['billitel']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['billitel']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['billitel']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['billitel']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['billitel']}/websms_send.php",
    },
    "educom": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['educom']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['educom']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['educom']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['educom']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['educom']}/websms_send.php",
    },
    "fenercell": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['fenercell']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['fenercell']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['fenercell']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['fenercell']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['fenercell']}/websms_send.php",
    },
    "georg": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['georg']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['georg']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['georg']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['georg']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['georg']}/websms_send.php",
    },
    "goood": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['goood']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['goood']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['goood']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['goood']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['goood']}/websms_send.php",
    },
    "kronemobile": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['kronemobile']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['kronemobile']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['kronemobile']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['kronemobile']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['kronemobile']}/websms_send.php",
    },
    "kuriermobil": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['kuriermobil']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['kuriermobil']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['kuriermobil']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['kuriermobil']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['kuriermobil']}/websms_send.php",
    },
    "simfonie": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['simfonie']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['simfonie']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['simfonie']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['simfonie']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['simfonie']}/websms_send.php",
    },
    "teleplanet": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['teleplanet']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['teleplanet']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['teleplanet']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['teleplanet']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['teleplanet']}/websms_send.php",
    },
    "wowww": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['wowww']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['wowww']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['wowww']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['wowww']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['wowww']}/websms_send.php",
    },
    "yooopi": {
        "LOGIN_URL": f"https://{PROVIDER_TLDS['yooopi']}/index.php",
        "LOGOUT_URL": f"https://{PROVIDER_TLDS['yooopi']}/index.php?dologout=2",
        "KONTOMANAGER_URL": f"https://{PROVIDER_TLDS['yooopi']}/kundendaten.php",
        "WEBSMS_FORM_URL": f"https://{PROVIDER_TLDS['yooopi']}/websms.php",
        "SEND_SMS_URL": f"https://{PROVIDER_TLDS['yooopi']}/websms_send.php",
    },
}

HELP = {
    "to_help": "Recipient phone number in the format: +436601234567",
    "desc": """Send an SMS via the yesss.at website. Some MVNOs that use
          the kontomanager.at interface are also supported.""",
    "configfile": "Path of a config-file. Default paths are: \
          '/etc/yessssms.conf' and '~/.config/yessssms.conf'. \
          An example file is yessssms_sample.conf.",
    "login": "Your phone number (eg. 06501234567), used to login at \
          yesss.at.\
          Or use the environment variable 'YESSSSMS_LOGIN'.",
    "password": """Your password, it\'s not recommended to use this. \
          Use a config-file instead (see: -c, --configfile).\
          Or use the environment variable 'YESSSSMS_PASSWD'.""",
    "check_login": """validates your login data""",
    "provider": f"""set a MVNO (mobile virtual network operator) other \
          than Yesss.at (default)\
          available are: {', '.join(list(PROVIDER_URLS.keys()))}""",
    "message": "Message to be sent by SMS",
    "version": "print version information.",
    "test": "send a test message to yourself",
    "print-config-file": "prints a sample config file, that can be piped \
          into eg. ~/.config/yessssms.conf.",
}
CONFIG_FILE_CONTENT = """\
# place this file, with correct credentials, at /etc/yessssms.conf
# or ~/.config/yessssms.conf
[YESSSSMS]
LOGIN =  06501234567
PASSWD = MySecre3tPassw0rd
# you can define a default recipient (will be overridden by -t option)
# DEFAULT_TO = +43664123123123

# define alternative MVNO (YESSS, EDUCOM, etc. see --help (--mvno))
# MVNO = YESSS

# # very advanced settings (be warned!!):
# [YESSSSMS_PROVIDER_URLS]

# # eg: EDUCOM:
# LOGIN_URL = https://educom.kontomanager.at/index.php
# LOGOUT_URL = https://educom.kontomanager.at/index.php?dologout=2
# KONTOMANAGER_URL = https://educom.kontomanager.at/kundendaten.php
# WEBSMS_FORM_URL = https://educom.kontomanager.at/websms.php
# SEND_SMS_URL = https://educom.kontomanager.at/websms_send.php
"""
# CONFIG_FILE_PATHS = []
CONFIG_FILE_PATHS = ["/etc/yessssms.conf", "~/.config/yessssms.conf"]

TEST_FORM_TOKEN_SAMPLE = (
    "<form action='websms_send.php' name='sms' id='smsform'"
    " method='post' onSubmit=\"return validate()\">"
    '<input type="hidden" name="token" value="f2ca1bb6c7e907d06dafe4687e579fc'
    "e76b37e4e93b7605022da52e6ccc26fd2\"><div class='form-group'>"
    "    <div class='input-row'>"
)
