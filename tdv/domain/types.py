from datetime import datetime
from typing import Tuple, Dict, List, Union, Any, Callable, TypeVar

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
UserId = int

# Custom types
Expirations = Tuple[Date, ...]
OptionChains = List[List[Union[Dict, Any]]]
OptionChainYF = Tuple[DataFrame, DataFrame, Dict]
OptionChainsYF = List[OptionChainYF]
Insertable = TypeVar('Insertable', bound=Union[int, str, float, bool, None, datetime])
Insertabless = List[List[Insertable]]
# NoReturnQuery = TypeVar('NoReturnQuery', bound=Union[Insert, Update, Delete])
NoReturnQuery = Union[Insert, Update, Delete]
# WhereAbleQuery = TypeVar('WhereAbleQuery', bound=Union[Any, Update, Delete])
WhereAbleQuery = Union[Any, Update, Delete]
UpdateParams = Dict[AttrName, Insertable]
Handler = Callable[..., None]
Args = Tuple[Any, ...]
KwArgs = Dict[str, Any]
