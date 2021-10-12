import pytest
from app.domain.exeptions import OutOfStock
from app.domain.models.Batch import Batch
from app.domain.models.OrderLine import OrderLine
from app.domain.models.allocate import allocate
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=today)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("shipment-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("shipment-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("shipment-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("oref", "MINIMALIST-SPOON", 10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch", "HIBROWN-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "HIBROWN-POSTER", 100, eta=today)
    line = OrderLine("oref", "HIBROWN-POSTER", 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "SMALL-FORK", 10, eta=None)
    allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine("order2", "SMALL-FORK", 2), [batch])
