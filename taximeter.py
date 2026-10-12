import time


class Taximeter:

    """Calcula la tarifa de una carrera según el tiempo parado y en movimiento"""

    def __init__(self, stopped_rate: float, movig_rate: float):

        self._stopped_rate = stopped_rate
        self._moving_rate = movig_rate
        self._in_progress = False

        self._is_moving = False
        self._segment_start = 0.0
        self._total = 0.0

    @property
    def in_progress(self) -> bool:
        return self._in_progress

    def start(self) -> None:
        self._in_progress = True
        self._is_moving = False
        self._total = 0.0
        self._segment_start = time.time()

    def set_moving(self, is_moving: bool) -> None:
        self._close_segment()
        self._is_moving = is_moving

    def _current_rate(self) -> float:
        return self._moving_rate if self._is_moving else self._stopped_rate

    def _close_segment(self) -> None:
        now = time.time()
        elapsed = now - self._segment_start
        self._total += elapsed * self._current_rate()
        self._segment_start = now
        
    def finish(self) -> float:
        self._close_segment()
        self._in_progress = False
        return self._total

