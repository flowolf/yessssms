"""Command line interface for YesssSMS."""
import argparse
import configparser
import logging
import sys
from datetime import datetime
from functools import wraps
from os.path import abspath
from os.path import expanduser

from YesssSMS import YesssSMS
from YesssSMS.const import CONFIG_FILE_CONTENT, CONFIG_FILE_PATHS, HELP, VERSION

MAX_MESSAGE_LENGTH_STDIN = 3 * 160


def cli_errors_handled(func):
    """Decorate and handle cli exceptions."""
    # pylint: disable-msg=R0911
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except YesssSMS.MissingLoginCredentialsError:
            print("error: no username or password defined (use --help for help)")
            sys.exit(2)
        except YesssSMS.ConnectionError:
            print(
                "error: could not connect to provider. "
                "check your Internet connection."
            )
            sys.exit(3)
        except YesssSMS.AccountSuspendedError:
            print(
                "error: your account was suspended because of 3 failed login attempts. "
                "try again in one hour."
            )
            sys.exit(4)
        except YesssSMS.SMSSendingError:
            print("error: could not send SMS")
            sys.exit(5)
        except YesssSMS.UnsupportedCharsError:
            print("error: message contains unsupported character(s)")
            sys.exit(6)
        except YesssSMS.EmptyMessageError:
            print("error: cannot send empty message.")
            sys.exit(7)
        except CLI.MissingSettingsError:
            print("error: missing settings or invalid settings.")
            sys.exit(8)

    return func_wrapper


class CLI:
    """CLI class for YesssSMS."""

    class MissingSettingsError(ValueError):
        """missing settings."""

    def __init__(self):
        """Init CLI."""
        self.config_files = CONFIG_FILE_PATHS
        self.yessssms = None
        self.message = None
        self.recipient = None
        self.exit_status = self.cli()

    @staticmethod
    def version_info():
        """Display version information."""
        print("yessssms {}".format(YesssSMS("", "").version()))

    @staticmethod
    def print_config_file():
        """Print a sample config file, to pipe into a file."""
        print(CONFIG_FILE_CONTENT, end="")

    @staticmethod
    def parse_args(args):
        """Parse arguments and return namespace."""
        parser = argparse.ArgumentParser(description=HELP["desc"])
        parser.add_argument("-t", "--to", dest="recipient", help=HELP["to_help"])
        parser.add_argument("-m", "--message", help=HELP["message"])
        parser.add_argument("-c", "--configfile", help=HELP["configfile"])
        parser.add_argument("-l", "--login", dest="login", help=HELP["login"])
        parser.add_argument("-p", "--password", dest="password", help=HELP["password"])
        parser.add_argument(
            "-T",
            "--check-login",
            action="store_true",
            default=False,
            help=HELP["check_login"],
        )
        parser.add_argument("--mvno", dest="provider", help=HELP["provider"])
        parser.add_argument(
            "--version", action="store_true", default=False, help=HELP["version"]
        )
        parser.add_argument(
            "--test", action="store_true", default=False, help=HELP["test"]
        )
        parser.add_argument(
            "--print-config-file",
            action="store_true",
            default=False,
            help=HELP["print-config-file"],
        )
        if not args:
            parser.print_help()
            return None

        return parser.parse_args(args)

    def read_config_files(self, config_file):
        """Read config files for settings."""
        if config_file:
            self.config_files.append(config_file)

        parsable_files = []
        for conffile in self.config_files:
            conffile = expanduser(conffile)
            conffile = abspath(conffile)
            parsable_files.append(conffile)

        login = None
        passwd = None
        default_recipient = None
        provider = None
        custom_provider_urls = None

        try:
            config = configparser.ConfigParser()
            config.read(parsable_files)

            login = str(config.get("YESSSSMS", "LOGIN"))
            passwd = str(config.get("YESSSSMS", "PASSWD"))

            if config.has_option("YESSSSMS", "DEFAULT_TO"):
                default_recipient = config.get("YESSSSMS", "DEFAULT_TO")
            if config.has_option("YESSSSMS", "MVNO"):
                provider = config.get("YESSSSMS", "MVNO")
            if config.has_option("YESSSSMS_PROVIDER_URLS", "LOGIN_URL"):
                custom_provider_urls = {
                    "LOGIN_URL": config.get("YESSSSMS_PROVIDER_URLS", "LOGIN_URL"),
                    "LOGOUT_URL": config.get("YESSSSMS_PROVIDER_URLS", "LOGOUT_URL"),
                    "KONTOMANAGER_URL": config.get(
                        "YESSSSMS_PROVIDER_URLS", "KONTOMANAGER_URL"
                    ),
                    "WEBSMS_URL": config.get("YESSSSMS_PROVIDER_URLS", "WEBSMS_URL"),
                }
        except (
            KeyError,
            configparser.NoSectionError,
            configparser.MissingSectionHeaderError,
        ) as ex:
            # only interested in missing settings if custom file is defined
            # else ignore it.
            if config_file:
                print("error: settings not found: {}".format(ex))
                raise self.MissingSettingsError()

        return (login, passwd, default_recipient, provider, custom_provider_urls)

    # inconsistent return (testing), too many branches
    # pylint: disable-msg=R1710,R0912
    @cli_errors_handled
    def cli(self):
        """Handle arguments for command line interface."""
        args = self.parse_args(sys.argv[1:])

        if not args:
            return 0

        if args.print_config_file:
            self.print_config_file()
            return 0
        if args.version:
            self.version_info()
            return 0

        (
            login,
            passwd,
            default_recipient,
            provider,
            custom_provider_urls,
        ) = self.read_config_files(args.configfile or None)

        if args.provider:
            provider = args.provider

        if args.login and args.password:
            login = args.login
            passwd = args.password

        logging.debug("login: %s", login)
        if provider:
            self.yessssms = YesssSMS(login, passwd, provider=provider)
        else:
            self.yessssms = YesssSMS(
                login, passwd, custom_provider=custom_provider_urls
            )

        if args.check_login:
            valid = self.yessssms.login_data_valid()
            text = ("ok", "") if valid else ("error", "NOT ")
            print("{}: login data is {}valid.".format(text[0], text[1]))
            return 0 if valid else 1

        if args.message == "-":
            message = ""
            for line in sys.stdin:
                message += line
                if len(message) > MAX_MESSAGE_LENGTH_STDIN:
                    break
            # maximum of 3 SMS if pipe is used
            message = message[:MAX_MESSAGE_LENGTH_STDIN]
        else:
            message = args.message

        if args.test:
            message = message or "yessssms (" + VERSION + ") test message at {}".format(
                datetime.now().isoformat()
            )
        recipient = args.recipient or default_recipient or login

        self.recipient = recipient
        self.message = message
        self.yessssms.send(default_recipient or recipient, self.message)
        return 0


def run():
    """Start and run the CLI."""
    CLI()
