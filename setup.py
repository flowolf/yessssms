from setuptools import setup, find_packages

VERSION = "0.1.1b3"

LONG_DESC = """\
YesssSMS
========
YesssSMS let's you send SMS via yesss.at's website. Regular rates apply and a
contract or prepaid plan is needed.

Use your website login and password.

This module is not suitable for batch SMS sending.
Each send() call logs in and out of yesss.at's website.

usage:
::

>>> from YesssSMS import YesssSMS
>>> sms = YesssSMS(YOUR_LOGIN, YOUR_PASSWORD)
>>> sms.send(TO_NUMBER, "Message")

"""

setup(
    name='YesssSMS',
    version=VERSION,
    description="YesssSMS let's you send SMS via yesss.at's website",
    long_description=LONG_DESC,
    url='https://github.com/flowolf/yessssms',
    author='Florian Klien',
    author_email='flowolf@klienux.org',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Communications :: Telephony',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    platforms='any',
    keywords=['SMS', 'Yesss', 'messaging'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # List run-time dependencies here.  These will be installed by pip
    install_requires=['requests'],

    # TODO
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'yessssms=yessssms:main',
    #     ],
    # },
)
