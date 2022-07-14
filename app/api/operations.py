from fastapi import APIRouter, Depends, Response, status
from typing import List, Optional

from app.models.auth import User
from app.models.operations import (
    Operation,
    OperationKind,
    OperationCreate,
    OperationUpdate,
)
from app.services.auth import get_current_user
from app.services.operations import OperationsService


router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/", response_model=List[Operation])
async def get_operations(
    kind: Optional[OperationKind] = None,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return await service.get_list(user.id, kind)


@router.get("/{operation_id}", response_model=Operation)
async def get_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return await service.get(user.id, operation_id)


@router.patch("/{operation_id}", response_model=Operation)
async def update_operation(
    operation_id: int,
    operation_data: OperationUpdate,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return await service.update(user.id, operation_id, operation_data)


@router.delete("/{operation_id}")
async def delete_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):
    await service.delete(user.id, operation_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/", response_model=Operation)
async def create_operation(
    operation_data: OperationCreate,
    user: User = Depends(get_current_user),
    service: OperationsService = Depends(),
):

    return await service.create(user.id, operation_data)
