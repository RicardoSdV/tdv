import os

import click

from tdv.constants import SOURCE_PATH


@click.group('format')
def format_group() -> None:
    """For code formatting commands"""


@format_group.command('quotes', help='Turns all double quotes into single')
def quotes() -> None:
    python_files = []
    for root, dirs, files in os.walk(SOURCE_PATH):
        for file in files:
            if file.endswith('.py') and not file.endswith('format.py'):
                python_files.append(os.path.join(root, file))

    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified_lines = []
        for line in lines:
            if '"""' in line:
                modified_lines.append(line)
            else:
                modified_lines.append(line.replace('"', "'"))

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)

    click.echo('Quotes formatting complete.')
