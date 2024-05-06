from math import isnan
from typing import TYPE_CHECKING, List, Dict, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
from tdv.domain.entities.option_entities.call_hist_entity import CallHist
from tdv.domain.entities.option_entities.put_hist_entity import PutHist
from tdv.domain.entities.option_entities.strike_entity import Strike

if TYPE_CHECKING:
    from tdv.infra.repos.option_repos.call_hist_repo import CallHistRepo
    from tdv.infra.repos.option_repos.put_hist_repo import PutHistRepo


class OptionHistService:
    def __init__(self, call_hist_repo: 'CallHistRepo', put_hist_repo: 'PutHistRepo') -> None:
        self.__call_hist_repo = call_hist_repo
        self.__put_hist_repo = put_hist_repo

    def create_option_hists(
        self, insert_time: InsertTime, strikes: List[Strike], calls: Dict, puts: Dict, conn: Connection
    ) -> Tuple[List[CallHist], List[PutHist]]:

        call_hists: List[CallHist] = []
        put_hists: List[PutHist] = []

        res_call: List[CallHist] = []
        res_put: List[PutHist] = []

        for option, Entity, repo, option_hists, res_option in zip(
            (calls, puts),
            (CallHist, PutHist),
            (self.__call_hist_repo, self.__put_hist_repo),
            (call_hists, put_hists),
            (res_call, res_put),
        ):

            for strike, last_trade_date, last_price, bid, ask, change, volume, open_interest, implied_volatility in zip(
                strikes,
                option['lastTradeDate'].values(),
                option['lastPrice'].values(),
                option['bid'].values(),
                option['ask'].values(),
                option['change'].values(),
                option['volume'].values(),
                option['openInterest'].values(),
                option['impliedVolatility'].values(),
            ):

                # print('last_trade_date', type(last_trade_date), last_trade_date)
                # print('last_price', type(last_price), last_price)
                # print('bid', type(bid), bid)
                # print('ask', type(ask), ask)
                # print('change', type(change), change)
                # print('volume', type(volume), volume)
                # print('open_interest', type(open_interest), open_interest)
                # print('implied_volatility', type(implied_volatility), implied_volatility)

                option_hist = Entity(
                    strike_id=strike.id,
                    insert_time_id=insert_time.id,
                    last_trade_date=last_trade_date,
                    last_price=last_price,
                    bid=bid,
                    ask=ask,
                    change=change,
                    volume=0 if isnan(volume) else int(volume),  # TODO: Comes as float from yf, should it be float?
                    open_interest=0 if isnan(open_interest) else int(open_interest),  # TODO: Same ^^^
                    implied_volatility=implied_volatility,
                )
                option_hists.append(option_hist)

            result = repo.insert(conn, option_hists)
            res_option.append(result)

        return res_call, res_put
