from datetime import datetime

from pydantic import BaseModel

from mcs.common import ManipulatorStatus


class Signal(BaseModel):
    start_time: int
    end_time: int
    status: ManipulatorStatus

    def to_display_value(self):
        return (
            f"[{datetime.fromtimestamp(self.start_time):%H:%M:%S} - "
            f"{datetime.fromtimestamp(self.end_time):%H:%M:%S} "
            f"{self.status.upper()}]"
        )
