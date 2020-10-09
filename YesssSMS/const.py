"""constants for YesssSMS."""
import json
import os

VERSION = json.loads(
    open(os.path.dirname(os.path.realpath(__file__)) + "/version.json").read()
)["version"]
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
        "WEBSMS_URL": "https://www.yesss.at/kontomanager.at/websms_send.php",
    },
    "billitel": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["billitel"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(
            PROVIDER_TLDS["billitel"]
        ),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["billitel"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["billitel"]),
    },
    "educom": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["educom"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(PROVIDER_TLDS["educom"]),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["educom"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["educom"]),
    },
    "fenercell": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["fenercell"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(
            PROVIDER_TLDS["fenercell"]
        ),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["fenercell"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["fenercell"]),
    },
    "georg": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["georg"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(PROVIDER_TLDS["georg"]),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(PROVIDER_TLDS["georg"]),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["georg"]),
    },
    "goood": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["goood"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(PROVIDER_TLDS["goood"]),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(PROVIDER_TLDS["goood"]),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["goood"]),
    },
    "kronemobile": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["kronemobile"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(
            PROVIDER_TLDS["kronemobile"]
        ),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["kronemobile"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["kronemobile"]),
    },
    "kuriermobil": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["kuriermobil"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(
            PROVIDER_TLDS["kuriermobil"]
        ),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["kuriermobil"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["kuriermobil"]),
    },
    "simfonie": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["simfonie"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(
            PROVIDER_TLDS["simfonie"]
        ),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["simfonie"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["simfonie"]),
    },
    "teleplanet": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["teleplanet"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(
            PROVIDER_TLDS["teleplanet"]
        ),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["teleplanet"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["teleplanet"]),
    },
    "wowww": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["wowww"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(PROVIDER_TLDS["wowww"]),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(PROVIDER_TLDS["wowww"]),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["wowww"]),
    },
    "yooopi": {
        "LOGIN_URL": "https://{}/index.php".format(PROVIDER_TLDS["yooopi"]),
        "LOGOUT_URL": "https://{}/index.php?dologout=2".format(PROVIDER_TLDS["yooopi"]),
        "KONTOMANAGER_URL": "https://{}/kundendaten.php".format(
            PROVIDER_TLDS["yooopi"]
        ),
        "WEBSMS_URL": "https://{}/websms_send.php".format(PROVIDER_TLDS["yooopi"]),
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
    "provider": """set a MVNO (mobile virtual network operator) other \
          than Yesss.at (default)\
          available are: {}""".format(
        ", ".join(list(PROVIDER_URLS.keys()))
    ),
    "message": "Message to be sent by SMS",
    "version": "print version information.",
    "test": "send a test message to yourself",
    "print-config-file": "prints a sample config file, that can be piped \
          into eg. ~/.config/yessssms.conf.",
}
CONFIG_FILE_CONTENT = """# place this file, with correct credentials, at /etc/yessssms.conf
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
# WEBSMS_URL = https://educom.kontomanager.at/websms_send.php
"""
# CONFIG_FILE_PATHS = []
CONFIG_FILE_PATHS = ["/etc/yessssms.conf", "~/.config/yessssms.conf"]
