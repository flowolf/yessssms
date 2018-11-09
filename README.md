# YesssSMS

[![Gitlab CI Badge](https://gitlab.com/flowolf/yessssms/badges/master/pipeline.svg)](https://gitlab.com/flowolf/yessssms/pipelines)[![coverage report](https://gitlab.com/flowolf/yessssms/badges/master/coverage.svg)](https://gitlab.com/flowolf/yessssms/commits/master)

YesssSMS let's you send SMS via yesss.at's website. Regular rates apply and a
contract or prepaid plan is needed.

Use your website login and password.

This module is not suitable for batch SMS sending.
Each send() call logs in and out of yesss.at's website.


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
