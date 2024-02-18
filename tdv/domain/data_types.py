from typing import Tuple, Dict, List, Union, Any

from pandas import DataFrame


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
