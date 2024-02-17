import click




@click.group('run')
def run_group() -> None:
    """Here you can run the different services such as Yahoo Finance or the APIs"""


@run_group.command('yf')
def yf() -> None:
    """Run periodic requests to Yahoo Finance to request options data"""
    from tdv.constants import ROOT_PATH
    from tdv.common_utils import declare_path
    from tdv.run import run

    declare_path(ROOT_PATH)
    run()
