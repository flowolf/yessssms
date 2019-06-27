from setuptools import setup, find_packages

DESC = "YesssSMS let's you send SMS via yesss.at's website"

version_file = open("YesssSMS/const.py")
VERSION = None
for c in version_file.readlines():
    c = c.strip()
    if not c.startswith("VERSION"):
        continue
    key, val = c.split('=')
    VERSION = val.strip().split('"')[1]

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()

setup(
    name='YesssSMS',
    version=VERSION,
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/flowolf/yessssms',
    author='Florian Klien',
    author_email='flowolf@klienux.org',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Communications :: Telephony',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    platforms='any',
    keywords=['SMS', 'Yesss', 'messaging'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'logo']),

    # List run-time dependencies here.  These will be installed by pip
    install_requires=['requests'],
    python_requires='>=3.3',

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'yessssms=YesssSMS.YesssSMS:cli',
        ],
    },
)
