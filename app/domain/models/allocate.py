from app.domain.exeptions import OutOfStock
from app.domain.models.OrderLine import OrderLine
from app.domain.models.Batch import Batch
from typing import List


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
    batch.allocate(line)
    return batch.reference
