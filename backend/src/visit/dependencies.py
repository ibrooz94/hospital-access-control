from typing import Any, Type
from fastapi import HTTPException, status
from sqlalchemy import select

from src.core.dependecies import SessionDep
from src.utils.types import ModelT



class VisitChecker:
    def __init__(self, item_model: Type[ModelT]):
        self.item_model = item_model

    async def __call__(self, visit_id: int, item_id: int, session:SessionDep):

        """
        Checks if an item object of a specific model is associated with a Visit object.

        Args:
            visit_id: ID of the parent object
            item_id: ID of the item object
            item_model: SQLAlchemy model class representing the item type

        Raises:
            HTTPException: 404 Not Found if item not found
            HTTPException: 413 Forbidded if item not found in parent

        Returns:
            Base: The retrieved item object
        """

        item_obj: ModelT = await session.get(self.item_model, item_id)
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
