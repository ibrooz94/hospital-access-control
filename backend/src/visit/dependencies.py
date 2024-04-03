
from typing import Any
from sqlalchemy import select

from fastapi import HTTPException, status
from src.core.dependecies import SessionDep



class VisitChecker:
    def __init__(self, item_model: Any):
        self.item_model = item_model

    async def __call__(self, visit_id: int, item_id: int, session:SessionDep):

        item_obj = await session.get(self.item_model, item_id)
        if not item_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.item_model.__name__} not found"
                )

        statement = select(self.item_model).where(getattr(self.item_model, "visit_id") == visit_id, 
                                                  getattr(self.item_model, "id") == item_obj.id)
        item = (await session.execute(statement)).scalar()
        
        if not item:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"{self.item_model.__name__} with ID {item_id} not found in visit with ID {visit_id}")

        return item
