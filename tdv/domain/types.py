from datetime import datetime
from typing import Tuple, Dict, List, Union, Any, Callable, TypeVar

from pandas import DataFrame
from sqlalchemy import Insert, Update, Delete

# Simple Types
TickerName = str
StrikeID = int
ExpiryID = int

# Custom types
IDs = List[int]

Expiries = Tuple[str, ...]
Options = List[List[Union[Dict, Any]]]
OptionChainYF = Tuple[DataFrame, DataFrame, Dict]
OptionChainsYF = List[OptionChainYF]
Insertable = TypeVar('Insertable', bound=Union[int, str, float, bool, None, datetime])
Insertabless = List[List[Insertable]]
NoReturnQuery = Union[Insert, Update, Delete]
WhereAbleQuery = Union[Any, Update, Delete]
UpdateParams = Dict[str, Insertable]
Handler = Callable[..., None]
Args = Tuple[Any, ...]
KwArgs = Dict[str, Any]


