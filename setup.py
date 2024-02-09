from setuptools import setup, find_packages


setup(
    name='tdv',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tdv = tdv.cli:cli_root'
        ]
    },
)
