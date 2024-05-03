from datetime import datetime
from typing import Tuple, Dict, List, Union, Any, Callable, TypeVar

from pandas import DataFrame
from sqlalchemy import Insert, Update, Delete

from tdv.domain.entities.expiry_entity import Expiry
from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.strike_entity import Strike

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

PfolOptionsByTickerName = Dict[TickerName, PortfolioOption]
StrikeByID = Dict[StrikeID, Strike]
ExpiryByID = Dict[ExpiryID, Expiry]
PfolOptionEssentials = Tuple[PfolOptionsByTickerName, StrikeByID, ExpiryByID]
