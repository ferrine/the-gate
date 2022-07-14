from dataclasses import dataclass
import threading
from typing import Optional, List
import time


@dataclass
class CarStatus:
    proximity: bool
    license_plate: Optional[List[str]]
    is_car: bool


@dataclass
class State:
    entrance: CarStatus
    exit: CarStatus
    gate_proximity: bool
    gate_open: bool


NoState = State(
    entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
    exit=CarStatus(proximity=False, license_plate=None, is_car=False),
    gate_proximity=False,
    gate_open=False,
)


class BaseSensor(threading.Thread):
    def __init__(self, event, name="sensor", interval=0.25) -> None:
        super().__init__(name=name, daemon=True)
        self._state = NoState
        self._update_event = event
        self._status_lock = threading.RLock()
        self.interval = interval

    def set_state(self, new_state: State):
        set_event = new_state != self._state
        with self._status_lock:
            self._state = new_state
        if set_event:
            self._update_event.set()
        else:
            self._update_event.clear()

    def get_state(self) -> State:
        return self._state

    def collect_state(self) -> State:
        return NoState

    def run(self) -> None:
        while True:
            state = self.collect_state()
            self.set_state(state)
            time.sleep(self.interval)
