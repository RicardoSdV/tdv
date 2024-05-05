from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.option_repos.put_hist_repo import PutHistRepo


class PutHistService:
    def __init__(self, db: 'DB', put_hist_repo: 'PutHistRepo') -> None:
        self.db = db
        self.put_hist_repo = put_hist_repo
