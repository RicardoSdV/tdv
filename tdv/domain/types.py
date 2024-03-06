from datetime import datetime
from typing import Tuple, Dict, List, Union, Any, Callable

from pandas import DataFrame
from sqlalchemy import Insert, Update, Delete, Select

# Strings
AttrName = str
Date = str
TickerName = str
TimeStr = str
TimeStamp = str
TimeZone = str

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
Insertable = Union[int, str, float, bool, None, datetime]
NoReturnQuery = Union[Insert, Update, Delete]
WhereAbleQuery = Union[Select, Update, Delete]
UpdateParams = Dict[AttrName, Insertable]
Handler = Callable[..., None]
Args = Tuple[Any, ...]
KwArgs = Dict[str, Any]
