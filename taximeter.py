import time


class Taximeter:

    """Calcula la tarifa de una carrera según el tiempo parado y en movimiento"""

    def __init__(self, stopped_rate: float, movig_rate: float):

        self._stopped_rate: stopped_rate
        self._moving_rate: movig_rate

        self._is_moving: False
        self._segment_start: 0.0
        self._total: 0.0

    def start(self) -> None:

        self._is_moving = False
        self._total = 0.0
        self._segment_start = time.time()