from fastapi import APIRouter, Depends, Response, status
from typing import List, Optional

from my_finance.models.auth import User
from my_finance.models.operations import (
    Operation,
    OperationKind,
    OperationCreate,
    OperationUpdate,
)
from my_finance.services.auth import get_current_user
from my_finance.services.operations import OperationsService


router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/", response_model=List[Operation])
def get_operations(
    kind: Optional[OperationKind] = None,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return service.get_list(user.id, kind)


@router.get("/{operation_id}", response_model=Operation)
def get_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return service.get(user.id, operation_id)


@router.patch("/{operation_id}", response_model=Operation)
def update_operation(
    operation_id: int,
    operation_data: OperationUpdate,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return service.update(user.id, operation_id, operation_data)


@router.delete("/{operation_id}")
def delete_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):
    service.delete(user.id, operation_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/", response_model=Operation)
def create_operation(
    operation_data: OperationCreate,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return service.create(user.id, operation_data)
