import threading
import time
from the_gate.sensor.base import BaseSensor, State, CarStatus, NoState


class DummySensor(BaseSensor):
    def __init__(self, *args, num=5, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.num = num

    def collect_state(self) -> State:
        self.counter += 1
        if self.counter > self.num:
            return State(
                entrance=CarStatus(proximity=True, license_plate=None, is_car=False),
                exit=CarStatus(proximity=False, license_plate=None, is_car=False),
                gate_proximity=False,
                gate_open=False,
            )
        else:
            return NoState


def test_event_notifies():
    event = threading.Event()
    sensor = DummySensor(event)
    start = time.time()
    sensor.start()
    if event.wait():
        end = time.time()
    assert end - start > 1
