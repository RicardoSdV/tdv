from typing import Tuple, Dict, List, Union, Any

from pandas import DataFrame


# Strings
TimeStr = str
TimeStamp = str
Date = str
TimeZone = str
TickerName = str

# Integers
Second = int
EntityId = int
ExchangeId = EntityId
TickerId = int
OptionChainId = int
OptionId = int

# Custom types
Expirations = Tuple[Date, ...]
OptionChains = List[List[Union[Dict, Any]]]
OptionChainYF = Tuple[DataFrame, DataFrame, Dict]
OptionChainsYF = List[OptionChainYF]
