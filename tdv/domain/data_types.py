from typing import Tuple, Dict, List, Union, Any, TYPE_CHECKING

from pandas import DataFrame

if TYPE_CHECKING:
    from tdv.domain.entities.exchange_entity import Exchange
    from tdv.domain.entities.option_chain_entity import OptionChain
    from tdv.domain.entities.option_entity import Option
    from tdv.domain.entities.ticker_entity import Ticker

# Built in types
TimeStr = str
TimeStamp = str
Date = str
TimeZone = str
TickerName = str
Second = int
ExchangeId = int

# Custom types
Expirations = Tuple[Date, ...]
OptionChains = List[List[Union[Dict, Any]]]
OptionChainYF = Tuple[DataFrame, DataFrame, Dict]
OptionChainsYF = List[OptionChainYF]
Entity = Union[Exchange, Ticker, OptionChain, Option]
