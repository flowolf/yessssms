## Testing YesssSMS

for testing run:

```
pytest
```

to test sending a live SMS add a `secrets.py` file with valid credentials into the tests folder

```
YESSS_LOGIN = "066412345678"
YESSS_PASSWD = "your password"
YESSS_TO = "06501234567"
```
and run:

```
pytest tests/yessssms_test_live.py
```
