import sys
from datetime import datetime, timedelta

import pandas_market_calendars as mcal

nyse = mcal.get_calendar('NYSE')

df = nyse.schedule(start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=10))

print(df.market_open[0])


