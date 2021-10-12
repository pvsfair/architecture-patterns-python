from typing import List, Set
from app.domain.models.Batch import Batch
from .abstract_repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, reference) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches: Set[Batch]) -> None:
        self._batches = set(batches)

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, reference) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[Batch]:
        return list(self._batches)
