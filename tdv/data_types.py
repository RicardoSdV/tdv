from typing import Tuple, Dict, List, Union, Hashable, Any

from pandas import DataFrame
from pandas_market_calendars import MarketCalendar
from schedule import Scheduler

# Built in types
TimeStr = str
TimeStamp = str
Date = str
TimeZone = str
ExchangeName = str
TickerName = str
Second = int

# Custom types
Expirations = Tuple[Date, ...]
OptionChains = List[List[Union[Dict, Any]]]
OptionChainYF = Tuple[DataFrame, DataFrame, Dict]
OptionChainsYF = List[OptionChainYF]
JsonSerializable = Union[int, str, float, bool, None, Dict[Hashable, 'JsonSerializable'], List['JsonSerializable'], Tuple['JsonSerializable', ...]]
