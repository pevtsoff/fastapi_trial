from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from my_finance import tables
from my_finance.database import get_session
from my_finance.models.operations import OperationKind, OperationCreate, OperationUpdate


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(
        self, user_id: int, kind: Optional[OperationKind]
    ) -> List[tables.Operation]:
        query = self.session.query(tables.Operation)

        if kind:
            query = query.filter_by(kind=kind)

        query = query.filter_by(user_id=user_id)

        return query.all()

    def create(self, user_id: int, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(**operation_data.dict(), user_id=user_id)
        self.session.add(operation)
        self.session.commit()
        return operation

    def get(self, user_id: int, operation_id) -> tables.Operation:
        return self._get(user_id, operation_id)

    def update(
        self, user_id: int, operation_id: int, operation_data: OperationUpdate
    ) -> tables.Operation:
        operation = self._get(user_id, operation_id)

        for field, value in operation_data:
            setattr(operation, field, value)

        self.session.commit()

        return operation

    def delete(self, user_id: int, operation_id: int):
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()

    def _get(self, user_id: int, operation_id: int) -> tables.Operation:
        operation = (
            self.session.query(tables.Operation)
            .filter_by(id=operation_id, user_id=user_id)
            .first()
        )

        if not operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"no opereation exists with id={operation_id}"},
            )

        return operation
