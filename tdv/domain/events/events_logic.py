""" Handle events logic in this file """


class EventsLogic:
    def on_market_open(self) -> None:
        """
        Start requesting
        Schedule market close
        """
        pass

    def on_market_close(self) -> None:
        """
        Stop requesting
        Schedule next market open
        """
        pass
