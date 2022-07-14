from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app import tables
from app.database import get_session
from app.models.operations import OperationKind, OperationCreate, OperationUpdate


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_list(
        self, user_id: int, kind: Optional[OperationKind]
    ) -> List[tables.Operation]:
        query = select(tables.Operation)


        if kind:
            query = select(tables.Operation).where(tables.Operation.kind==kind)
        else:
            query = select(tables.Operation).where(tables.Operation.user_id==user_id)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, user_id: int, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(**operation_data.dict(), user_id=user_id)
        self.session.add(operation)
        await self.session.commit()
        return operation

    async def get(self, user_id: int, operation_id) -> tables.Operation:
        return await self._get(user_id, operation_id)

    async def update(
        self, user_id: int, operation_id: int, operation_data: OperationUpdate
    ) -> tables.Operation:
        operation = self._get(user_id, operation_id)

        for field, value in operation_data:
            setattr(operation, field, value)

        await self.session.commit()

        return operation

    async def delete(self, user_id: int, operation_id: int):
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        await self.session.commit()

    async def _get(self, user_id: int, operation_id: int) -> tables.Operation:
        # operation = (
        #     self.session.query(tables.Operation)
        #     .filter_by(id=operation_id, user_id=user_id)
        #     .first()
        # )
        query = select(tables.Operation).where(id=operation_id, user_id=user_id)
        result = await self.session.execute(query)
        operation = result.scalars().first()

        if not operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"no opereation exists with id={operation_id}"},
            )

        return operation
