from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.call_hist_repo import CallHistRepo


class CallHistService:
    def __init__(self, db: 'DB', call_hist_repo: 'CallHistRepo') -> None:
        self.db = db
        self.call_hist_repo = call_hist_repo
