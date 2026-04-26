from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.address_service import AddressService
from app.schemas.address_schema import AddressCreate, AddressUpdate, AddressRead


router = APIRouter(prefix="/addresses", tags=["Address Center"])

@router.get(
    "/",
    response_model=list[AddressRead],
    summary="Get All Addresses",
    description="Retrieve a list of all addresses in the system.",
    responses={
        200: {"description": "List of addresses retrieved successfully."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_addresses(
    db: AsyncSession = Depends(get_db_connection)
):
    address_service = AddressService(db)
    return await address_service.get_all_addresses()

@router.get(
    "/{address_id}",
    response_model=AddressRead,
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
    db: AsyncSession = Depends(get_db_connection)
):
    address_service = AddressService(db)
    return await address_service.get_address_by_id(address_id)

@router.get(
    "/get-by-cep/{cep}",
    response_model=list[AddressRead],
    summary="Get Addresses by CEP",
    description="Retrieve a list of addresses by their CEP (postal code).",
    responses={
        200: {"description": "Addresses retrieved successfully."},
        500: {"description": "Internal server error."}
    }
)
async def get_addresses_by_cep(
    cep: str,
    db: AsyncSession = Depends(get_db_connection)
):
    address_service = AddressService(db)
    return await address_service.get_addresses_by_cep(cep)

@router.put(
    "/{address_id}",
    response_model=AddressRead,
    summary="Update Address",
    description="Update an existing address by its unique ID.",
    responses={
        200: {"description": "Address updated successfully."},
        404: {"description": "Address not found."},
        500: {"description": "Internal server error."}
    }
)
async def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: AsyncSession = Depends(get_db_connection)
):
    address_service = AddressService(db)
    return await address_service.update_address(address_id, address_update)