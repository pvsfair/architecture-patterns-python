from abc import ABC, abstractmethod
from typing import List

from app.domain.models.Batch import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Batch]:
        raise NotImplementedError
