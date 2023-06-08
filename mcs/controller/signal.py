from datetime import datetime

from pydantic import BaseModel

from mcs.common import ManipulatorStatus


class Signal(BaseModel):
    start_time: datetime
    end_time: datetime
    status: ManipulatorStatus

    def to_display_value(self):
        return (
            f"[{self.start_time:%H:%M:%S} - "
            f"{self.end_time:%H:%M:%S} "
            f"{self.status.upper()}]"
        )
