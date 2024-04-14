from typing import Any, Dict, Optional, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.types import ModelT



class CRUDBase:
    """
    Base class for CRUD operations on SQLAlchemy models.

    Type arguments:
        Model (SQLAlchemy.orm.decl_api.DeclarativeBase): The SQLAlchemy model class.
    """

    def __init__(self, model: type[ModelT]):
        self.model = model

    async def create(self, session: AsyncSession, data: Dict[str, Any], *args, **kwargs) -> ModelT:
        """
        Creates a new instance of the model.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            data (Dict[str, Any]): The data to be used for creating the model instance.

        Returns:
            Any: The newly created model instance.

        Raises:
            HTTPException: If there is an error during creation.
        """

        try:
            db_obj = self.model(**data)  # Unpack data directly into model attributes
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error creating {self.model.__name__}: {str(e)}",
            )

    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[ModelT]:
        """
        Retrieves all instances of the model.

        Args:
            session (AsyncSession): The SQLAlchemy session object.

        Returns:
            list[Any]: A list of all model instances.
        """

        query = select(self.model).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, id: int) -> Optional[ModelT]:
        """
        Retrieves a single instance of the model by its ID.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            id (int): The ID of the model instance to retrieve.

        Returns:
            Optional[Any]: The requested model instance, or None if not found.
        """

        query = select(self.model).where(self.model.id == id)
        result = (await session.execute(query)).scalar()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found"
            )
        return result 
    
    async def update(self, session: AsyncSession, id: int, data: Dict[str, Any]) -> Optional[ModelT]:
        """
        Updates an existing instance of the model.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            id (int): The ID of the model instance to update.
            data (Dict[str, Any]): The data to be used for updating the model instance.

        Returns:
            Optional[Any]: The updated model instance, or None if not found.

        Raises:
            HTTPException: If there is an error during update.
        """

        db_obj = await self.get_by_id(session, id)

        try:
            for key, value in data.items():
                setattr(db_obj, key, value)  # Dynamically update model attributes

            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error updating {self.model.__name__}: {str(e)}",
            )

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """
        Deletes an existing instance of the model by its ID.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            id (int): The ID of the model instance to delete.

        Returns:
            int: The deleted model's ID (if successful), or raises an exception.
        """

        db_obj = await self.get_by_id(session, id)

        try:
            await session.delete(db_obj)
            await session.commit()
            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error deleting object: {str(e)}",
            )