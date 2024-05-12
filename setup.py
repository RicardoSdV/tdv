from setuptools import setup, find_packages

from tdv.constants import CLI, BUILD

setup(
    name=BUILD.NAME,
    version=BUILD.VERSION,
    packages=find_packages(),
    entry_points={'console_scripts': [CLI.CONSOLE_ENTRY]},
)
