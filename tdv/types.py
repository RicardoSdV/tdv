from typing import Tuple, Dict, List, Union, Hashable, Any

from pandas import DataFrame

# Built in types
TimeStamp = str
Date = str
Time = str
TimeZone = str
ExchangeName = str
Second = int

# Custom types
Expirations = Tuple[Date, ...]
OptionChains = List[List[Union[Dict, Any]]]
OptionChainYF = Tuple[DataFrame, DataFrame, Dict]
OptionChainsYF = List[OptionChainYF]
JsonSerializable = Union[int, str, float, bool, None, Dict[Hashable, 'JsonSerializable'], List['JsonSerializable'], Tuple['JsonSerializable', ...]]
