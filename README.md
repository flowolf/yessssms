# YesssSMS

[![Python version](https://img.shields.io/pypi/pyversions/yessssms.svg)](https://gitlab.com/flowolf/yessssms) [![Gitlab CI Badge](https://gitlab.com/flowolf/yessssms/badges/master/pipeline.svg)](https://gitlab.com/flowolf/yessssms/pipelines) [![coverage report](https://gitlab.com/flowolf/yessssms/badges/master/coverage.svg)](https://gitlab.com/flowolf/yessssms/commits/master) [![pypi version](https://img.shields.io/pypi/v/yessssms.svg?color=blue)](https://pypi.org/project/yessssms) [![dev version](https://img.shields.io/badge/dynamic/json?color=yellow&label=dev&query=version&url=https%3A%2F%2Fgitlab.com%2Fflowolf%2Fyessssms%2Fraw%2Fmaster%2FYesssSMS%2Fversion.json&prefix=v)](https://gitlab.com/flowolf/yessssms) [![license](https://img.shields.io/pypi/l/yessssms.svg)](https://gitlab.com/flowolf/yessssms/blob/master/LICENSE.txt) [![documentation](https://img.shields.io/badge/sphinx-docs-blue)](https://flowolf.gitlab.io/yessssms/) [![downloads](https://img.shields.io/pypi/dm/yessssms)](https://pypi.org/project/yessssms)

YesssSMS let's you send SMS via yesss.at's website. Regular rates apply and a
contract or prepaid plan is needed.


Alternatively you can use MVNOs (Mobile Virtual Network Operators) that use the kontomanager.at web interface.
These include:
* YESSS
* billitel
* EDUCOM
* fenercell
* georg
* goood
* kronemobile
* kuriermobil
* SIMfonie
* teleplanet
* WOWWW
* yooopi

![all provider logos](https://gitlab.com/flowolf/yessssms/raw/master/logo/all.png "supported providers")

Use your website login and password.

use the `--mvno` flag to set your provider, or define it in the config file.

This module is not suitable for batch SMS sending.
Each send() call logs in and out of your provider's website.

Currently the library supports Python 3.5+, and is [tested against Python 3.5 to 3.9](https://gitlab.com/flowolf/yessssms/-/jobs).

### Install
```bash
> pip3 install YesssSMS
```

### Usage
```python
>>> from YesssSMS import YesssSMS
>>> sms = YesssSMS(YOUR_LOGIN, YOUR_PASSWORD)
>>> sms.send(TO_NUMBER, "Message")
>>> # or with a different MVNO:
>>> sms = YesssSMS(YOUR_LOGIN, YOUR_PASSWORD, provider="goood")
>>> sms.send(TO_NUMBER, "Message")
```

```python
# environment variables set
>>> from YesssSMS import YesssSMS
>>> sms = YesssSMS()
>>> sms.send("hello future self, your pipeline failed :(")
```

### Command Line Usage
```bash
> yessssms --print-config-file > ~/.config/yessssms.conf
# edit the config file, set a login, password, default recipient, and MVNO
> vi ~/.config/yessssms.conf
> yessssms --test # test your setup, send yourself a message
> yessssms -t 0664123123123 -m "sending SMS from the command line :)"

> # if a default recipient is defined, you can omit the -t flag
> # the message can be piped into yessssms (it will be cut to max 3 SMS, 3*160 chars)
> echo "important message!" | yessssms -m -

> # MVNO
> yessssms --to 06501234567 --mvno educom -m "sending SMS using a MVNO"
```

```bash
# set environment variables to avoid parameters or config files;
# great for pipelines
> export YESSSSMS_LOGIN=06641234567
> export YESSSSMS_PASSWD=myverysecretsecret
# use in python script or in command line
> yessssms -T
ok: login data is valid.
> yessssms -m "sending SMS from github and gitlab pipelines... so much cloud"
```
