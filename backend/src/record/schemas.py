
from pydantic import BaseModel

class PermissionCreate(BaseModel):
    user_id: int
    record_id: int
    can_edit: bool
    can_view: bool

