# YesssSMS

[![Python version](https://img.shields.io/pypi/pyversions/yessssms.svg)](https://gitlab.com/flowolf/yessssms) [![Gitlab CI Badge](https://gitlab.com/flowolf/yessssms/badges/master/pipeline.svg)](https://gitlab.com/flowolf/yessssms/pipelines) [![coverage report](https://gitlab.com/flowolf/yessssms/badges/master/coverage.svg)](https://gitlab.com/flowolf/yessssms/commits/master) [![pypi version](https://img.shields.io/pypi/v/yessssms.svg?color=blue)](https://pypi.org/project/yessssms) [![license](https://img.shields.io/pypi/l/yessssms.svg)](https://gitlab.com/flowolf/yessssms/blob/master/LICENSE.txt)

YesssSMS let's you send SMS via yesss.at's website. Regular rates apply and a
contract or prepaid plan is needed.

Use your website login and password.

Alternatively you can use MVNOs (Mobile Virtual Network Operators) that use the kontomanager.at web interface.
These include:
* YESSS
* EDUCOM
* SIMfonie
* ...

use the `--mvno` flag to set your provider, or define the used URLs in the config file.


This module is not suitable for batch SMS sending.
Each send() call logs in and out of yesss.at's website.

Currently the library supports Python 3.5+, and is [tested against Python 3.5 to 3.7](https://gitlab.com/flowolf/yessssms/-/jobs).

### Install
```bash
> pip3 install YesssSMS
```
### Usage
```python
>>> from YesssSMS import YesssSMS
>>> sms = YesssSMS(YOUR_LOGIN, YOUR_PASSWORD)
>>> sms.send(TO_NUMBER, "Message")
```
or for the command line:
```bash
> yessssms --print-config-file > ~/.config/yessssms.conf
# edit the config file
> vi ~/.config/yessssms.conf
> yessssms --test # test your setup, send yourself a message
> yessssms -t 0664123123123 -m "sending SMS from the command line :)"

> # if a default recipient is defined, you can omit the -t flag
> # the message can be piped into yessssms (it will be cut to max 3 SMS, 3*160 chars)
> echo "important message!" | yessssms -m -

> # MVNO
> yessssms --t 06501234567 --mvno EDUCOM -m 'testmessage ;)'

```
