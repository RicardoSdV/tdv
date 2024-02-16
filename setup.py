from setuptools import setup, find_packages

from tdv.constants import BUILD_NAME, BUILD_VERSION, CLI_ROOT_COMMAND, SOURCE_CODE_DIR_NAME, CLI_ROOT_FUNC_NAME

setup(
    name=BUILD_NAME,
    version=BUILD_VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            f'{CLI_ROOT_COMMAND} = {SOURCE_CODE_DIR_NAME}.cli:{CLI_ROOT_FUNC_NAME}'
        ]
    },
)
