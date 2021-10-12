from typing import Optional, Set
from datetime import date

from app.domain.models.OrderLine import OrderLine


class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Batch):
            return False
        return o.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, o: object):
        if self.eta is None:
            return False
        if o.eta is None:
            return True
        return self.eta > o.eta

    def __repr__(self):
        return f"<Batch {self.reference}>"
