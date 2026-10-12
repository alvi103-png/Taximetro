import pytest

import taximeter
from taximeter import Taximeter

STOPPED_RATE = 0.02
MOVING_RATE = 0.05


class FakeClock:
    """Reloj falso: el tiempo solo avanza cuando llamamos a advance()"""

    def __init__(self):
        self.now = 0.0

    def time(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def clock(monkeypatch):
    """Sustituye time.time() dentro de taximeter.py por el reloj falso"""
    fake = FakeClock()
    monkeypatch.setattr(taximeter.time, "time", fake.time)
    return fake


def test_stopped_trip_charges_stopped_rate(clock):
    meter = Taximeter(STOPPED_RATE, MOVING_RATE)

    meter.start()
    clock.advance(10)
    total = meter.finish()

    assert total == pytest.approx(0.20)

def test_moving_trip_charges_moving_rate(clock):
    meter = Taximeter(STOPPED_RATE, MOVING_RATE)

    meter.start()
    meter.set_moving(True)
    clock.advance(20)
    total = meter.finish()

    assert total == pytest.approx(1)

def test_mixed_trip_combines_both_rates(clock):
    meter = Taximeter(STOPPED_RATE, MOVING_RATE)

    meter.start()
    clock.advance(10)
    meter.set_moving(True)
    clock.advance(20)
    total = meter.finish()

    assert total == pytest.approx(1.2)

def test_new_trip_starts_from_zero(clock):
    meter = Taximeter(STOPPED_RATE, MOVING_RATE)

    meter.start()
    meter.set_moving(True)
    clock.advance(10)
    meter.finish()

    clock.advance(60)

    meter.start()
    meter.set_moving(True)
    clock.advance(30)
    second_total = meter.finish()

    assert second_total == pytest.approx(1.5)

def test_in_progress_follows_trip_lifecycle(clock):
    meter = Taximeter(STOPPED_RATE, MOVING_RATE)

    meter.set_moving(False)
    assert meter.in_progress is False

    meter.start()
    meter.set_moving(True)
    assert meter.in_progress is True

    meter.finish()
    assert meter.in_progress is False



    