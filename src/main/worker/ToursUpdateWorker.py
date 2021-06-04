from __future__ import annotations

from typing import Any

from pykka import ThreadingActor


class ToursUpdateWorker(ThreadingActor):

    def __init__(self):
        super().__init__()

    def on_receive(self, message: Any) -> Any:
        if isinstance(message, ToursUpdateMessage):
            self.execute_update(message)

    def execute_update(self, message: ToursUpdateMessage):
        print('EXECUTE UPDATE')
        self.stop()


class ToursUpdateMessage:

    def __init__(self):
        pass
