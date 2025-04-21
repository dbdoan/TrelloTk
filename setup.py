from setuptools import setup

APP = ['main.py']
DATA_FILES = ['config.json', 'key.db']
OPTIONS = {
    'iconfile': 'icon.icns',
    'packages': ['tkinter'],
    'includes': ['clipboard', 'nav_trl', 'pkg_resources', 'jaraco.text'],
    'resources': ['img'],
    'excludes': ['packaging', 'tomli', 'typeguard'],
    'plist': {
        'CFBundleName': 'TkTrello',
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0',
        'CFBundleIdentifier': 'com.dannydoan.tktrello',
    },
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)