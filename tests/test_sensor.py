import threading
import time
from the_gate.sensor.base import BaseSensor, State, CarStatus, NoState, GateStatus


car_rides_inside_case = [
    (NoState, 5 / 10),
    (
        State(
            entrance=CarStatus(proximity=True, license_plate=None, is_car=False),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Closed,
        ),
        3 / 10,
    ),
    (
        State(
            entrance=CarStatus(
                proximity=True, license_plate=["1", "4", "A"], is_car=True
            ),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Closed,
        ),
        2 / 10,
    ),
    (
        State(
            entrance=CarStatus(
                proximity=True, license_plate=["1", "4", "A"], is_car=True
            ),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Unclear,
        ),
        7 / 10,
    ),
    (
        State(
            entrance=CarStatus(
                proximity=True, license_plate=["1", "4", "A"], is_car=True
            ),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Open,
        ),
        3 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=True, license_plate=None, is_car=False),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=True,
            gate_status=GateStatus.Open,
        ),
        3 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=True,
            gate_status=GateStatus.Open,
        ),
        3 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
            exit=CarStatus(proximity=True, license_plate=None, is_car=False),
            gate_proximity=True,
            gate_status=GateStatus.Open,
        ),
        3 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
            exit=CarStatus(proximity=True, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Open,
        ),
        3 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
            exit=CarStatus(proximity=True, license_plate=["1", "4", "A"], is_car=True),
            gate_proximity=False,
            gate_status=GateStatus.Open,
        ),
        0.25 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
            exit=CarStatus(proximity=True, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Unclear,
        ),
        5 / 10,
    ),
    (
        State(
            entrance=CarStatus(proximity=False, license_plate=None, is_car=False),
            exit=CarStatus(proximity=False, license_plate=None, is_car=False),
            gate_proximity=False,
            gate_status=GateStatus.Unclear,
        ),
        5 / 10,
    ),
    (NoState, 15),
]


class DummySensor(BaseSensor):
    def __init__(self, *args, sequence, repeat=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.sequence = sequence
        self.repeat = repeat

    def run(self) -> None:
        self.counter = 0
        self.last_update = time.time()
        return super().run()

    def collect_state(self) -> State:
        _, duration = self.sequence[self.counter]
        if (time.time() - self.last_update) > duration:
            self.counter += 1
            self.last_update = time.time()
        return self.sequence[self.counter][0]


def test_event_notifies():
    event = threading.Event()
    sensor = DummySensor(event, sequence=car_rides_inside_case, interval=0.01)
    sensor.start()
    events = 0
    while event.wait(timeout=10):
        e = sensor.get_state()
        print(e)
        event.clear()
        events += 1
    assert events == len(car_rides_inside_case)
