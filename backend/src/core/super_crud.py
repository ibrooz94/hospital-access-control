from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict

from .crud import CRUDBase

class BulkCRUDAdapter(CRUDBase):
    """
    Adapter for CRUD operations with bulk insert, update, and delete (for superusers only).

    Type arguments:
        Model (SQLAlchemy.orm.decl_api.DeclarativeBase): The SQLAlchemy model class.
    """

    async def bulk_insert(self, session: AsyncSession, data_list: list[Dict[str, Any]]) -> None:
        """
        Inserts multiple instances of the model in bulk.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            data_list (list[Dict[str, Any]]): A list of dictionaries containing data for each model instance.

        """

        try:
            db_objects = [self.model(**data) for data in data_list]
            session.add_all(db_objects)
            await session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error creating objects: {str(e)}",
            )

    async def bulk_update(self, session: AsyncSession, data_list: list[Dict[str, Any]]) -> None:
        """
        Updates multiple instances of the model in bulk based on IDs and data.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            data_list (list[Dict[str, Any]]): A list of dictionaries containing the ID and updated data for each model instance.

        """

        try:
            for data in data_list:
                id = data.get("id")
                if not id:
                    raise ValueError("Missing ID in update data")
                db_obj = await self.get_by_id(session, id)
                if not db_obj:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
                    )
                for key, value in data.items():
                    if key != "id":  # Skip updating the ID field
                        setattr(db_obj, key, value)
            session.add_all(db_obj for db_obj in data_list if db_obj)  # Update only retrieved objects
            await session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error updating objects: {str(e)}",
            )

    async def bulk_delete(self, session: AsyncSession, id_list: list[int]) -> None:
        """
        Deletes multiple instances of the model in bulk based on their IDs.

        Args:
            session (AsyncSession): The SQLAlchemy session object.
            id_list (list[int]): A list of IDs for the model instances to be deleted.

        """

        try:
            query = select(self.model).where(self.model.id.in_(id_list))
            result = await session.execute(query)
            db_objects = result.scalars().all()
            if not db_objects:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No objects found for deletion"
                )
            session.delete(*db_objects)  # Efficient bulk deletion using unpack operator
            await session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error deleting objects: {str(e)}",
            )
