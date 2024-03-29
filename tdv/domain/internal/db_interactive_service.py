from typing import TYPE_CHECKING, Callable, List, TypeVar

from tdv.domain.entities.base_entity import Entity

if TYPE_CHECKING:
    from tdv.infra.repos.base_repo import BaseRepo
    from tdv.infra.database import DB

EntityT = TypeVar('EntityT', bound='Entity')


class DbInteractiveService:
    def __init__(self, db: 'DB', repo: 'BaseRepo') -> None:
        self._db = db
        self._repo = repo

    def _do_db_operation(self, method: Callable, entities: List[Entity], *args, **kwargs) -> List[Entity]:
        """Call a single repo method"""
        with self._db.connect as conn:
            entities = method(conn, entities, *args, **kwargs)
            conn.commit()
        return entities
