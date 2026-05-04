from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.address_service import AddressService
from app.schemas.address_schema import AddressUpdate, AddressRead
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse
from app.auth.jwt_handler import get_current_user
from app.auth.dependencies import require_admin, require_admin_or_driver
from app.core.exceptions import ForbiddenException
from app.models.enums import UserRole
from app.models.user import User


router = APIRouter(prefix="/api/v1/addresses", tags=["Address Center"])

@router.get(
    "/",
    response_model=PaginatedResponse[AddressRead],
    status_code=status.HTTP_200_OK,
    summary="Get All Addresses",
    description="Retrieve a paginated list of all addresses in the system.",
    responses={
        200: {"description": "List of addresses retrieved successfully."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_addresses(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    params = PaginationParams(page=page, size=size)
    address_service = AddressService(db)
    return await address_service.get_all_addresses(params)

@router.get(
    "/{address_id}",
    response_model=AddressRead,
    status_code=status.HTTP_200_OK,
    summary="Get Address by ID",
    description="Retrieve an address by its unique ID.",
    responses={
        200: {"description": "Address retrieved successfully."},
        404: {"description": "Address not found."},
        500: {"description": "Internal server error."}
    }
)
async def get_address_by_id(
    address_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    address_service = AddressService(db)
    return await address_service.get_address_by_id(address_id)

@router.get(
    "/get-by-cep/{cep}",
    response_model=PaginatedResponse[AddressRead],
    status_code=status.HTTP_200_OK,
    summary="Get Addresses by CEP",
    description="Retrieve a paginated list of addresses by their CEP (postal code).",
    responses={
        200: {"description": "Addresses retrieved successfully."},
        404: {"description": "No addresses found for the given CEP."},
        500: {"description": "Internal server error."}
    }
)
async def get_addresses_by_cep(
    cep: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    params = PaginationParams(page=page, size=size)
    address_service = AddressService(db)
    return await address_service.get_addresses_by_cep(cep, params)

@router.put(
    "/{address_id}",
    response_model=AddressRead,
    status_code=status.HTTP_200_OK,
    summary="Update Address",
    description="Update an existing address by its unique ID.",
    responses={
        200: {"description": "Address updated successfully."},
        403: {"description": "Forbidden."},
        404: {"description": "Address not found."},
        500: {"description": "Internal server error."}
    }
)
async def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_role == UserRole.DRIVER:
        raise ForbiddenException("Drivers do not have permission to update addresses.")
    
    if current_user.user_role == UserRole.CUSTOMER and current_user.address_id != address_id:
        raise ForbiddenException("You do not have permission to update this address.")
    address_service = AddressService(db)
    return await address_service.update_address(address_id, address_update)
