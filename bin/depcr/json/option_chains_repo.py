from pathlib import Path
from typing import Optional

from pandas import DataFrame

from tdv.constants import TESLA_EXPIRATIONS_DIR_PATH
from tdv.domain.types import OptionChains, OptionChainsYF
from bin.depcr.json.base_repo import BaseRepo, BaseSerializer, BasePathBuilder


class OptionChainsSerializer(BaseSerializer):
    @staticmethod
    def serialize_yf_option_chains(option_chains: OptionChainsYF) -> OptionChains:
        return [
            [el.to_dict() if isinstance(el, DataFrame) else el for el in option_chain]
            for option_chain in option_chains
            if all(isinstance(el, (DataFrame, dict)) for el in option_chain)
        ]


class OptionChainsPathBuilder(BasePathBuilder):
    @classmethod
    def get_timestamp_tesla_expirations_path(cls) -> Path:
        return cls._get_timestamp_path(TESLA_EXPIRATIONS_DIR_PATH)


class OptionChainsRepo(OptionChainsPathBuilder, OptionChainsSerializer, BaseRepo):
    @classmethod
    def save(cls, option_chains: OptionChainsYF, indent: Optional[int] = None) -> None:
        path = cls.get_timestamp_tesla_expirations_path()
        serialized_data = cls.serialize_yf_option_chains(option_chains)
        cls._save_to_json(path, serialized_data, cls._turn_to_str, indent)
