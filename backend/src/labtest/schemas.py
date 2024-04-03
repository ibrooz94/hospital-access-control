from enum import Enum

class LabStatus(str, Enum):
    REQUESTED = "requested"
    PENDING = "pending"
    COMPLETED = "completed"

