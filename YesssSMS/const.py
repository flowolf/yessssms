"""constants for YesssSMS."""
VERSION = "0.4.0b1"
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
# <div class='alert alert-warning'>Lieber yesss! Kunde,<br /><br />Ihre Karte \
# wurde deaktiviert, da Sie innerhalb der letzten 12 Monate nicht mehr \
# aufgeladen haben. Bitte laden Sie zur Aktivierung Ihrer SIM-Karte Ihr \
# Guthaben wieder auf, da andernfalls in Kürze die Rufnummer gelöscht wird.\
# <br /><br />Ihr yesss! Team</div>
_ACCOUNT_LOCKED_WARNING = ">Ihre Karte wurde deaktiviert, da Sie innerhalb \
der letzten 12 Monate nicht mehr aufgeladen haben."

PROVIDER_URLS = {
  'YESSS': {
            'LOGIN_URL': "https://www.yesss.at/kontomanager.at/index.php",
            'LOGOUT_URL': "https://www.yesss.at/kontomanager.at/index.php?dologout=2",
            'KONTOMANAGER_URL': "https://www.yesss.at/kontomanager.at/kundendaten.php",
            'WEBSMS_URL': "https://www.yesss.at/kontomanager.at/websms_send.php" 
          },
  'EDUCOM': {
            'LOGIN_URL': "https://educom.kontomanager.at/index.php",
            'LOGOUT_URL': "https://educom.kontomanager.at/index.php?dologout=2",
            'KONTOMANAGER_URL': "https://educom.kontomanager.at/kundendaten.php",
            'WEBSMS_URL': "https://educom.kontomanager.at/websms_send.php" 
          },
  'SIMfonie': {
            'LOGIN_URL': "https://simfonie.kontomanager.at/index.php",
            'LOGOUT_URL': "https://simfonie.kontomanager.at/index.php?dologout=2",
            'KONTOMANAGER_URL': "https://simfonie.kontomanager.at/kundendaten.php",
            'WEBSMS_URL': "https://simfonie.kontomanager.at/websms_send.php"
          }
}

HELP = {'to_help': 'Recipient phone number in the format: +436601234567',
        'desc': 'Send an SMS via the yesss.at website',
        'configfile': "Path of a config-file. Default paths are: \
          '/etc/yessssms.conf' and '~/.config/yessssms.conf'. \
          An example file is yessssms_sample.conf.",
        'login': 'Your phone number (eg. 06501234567), used to login at \
          yesss.at',
        'password': """Your password, it\'s not recommended to use this. \
          Use a config-file instead (see: -c, --configfile).""",
        'provider': """set a MVNO (mobile virtual network operator) other than Yesss.at (default)\
          available are: {}""".format(list(PROVIDER_URLS.keys())),
        'message': 'Message to be sent by SMS',
        'version': 'print version information.',
        'test': 'send a test message to yourself',
        'print-config-file': 'prints a sample config file, that can be piped \
          into eg. ~/.config/yessssms.conf.',
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
CONFIG_FILE_PATHS = ["/etc/yessssms.conf",
                     "~/.config/yessssms.conf",
                    ]
