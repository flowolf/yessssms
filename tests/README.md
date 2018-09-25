## Testing YesssSMS

for testing, add a `secrets.py` file with valid credentials into the tests folder

```
YESSS_LOGIN = "066412345678"
YESSS_PASSWD = "your password"
YESSS_TO = "06501234567"
```
and run

```
pytest -k "not test_send_sms"
```

to test everything, including sending a test SMS:
```
pytest
```