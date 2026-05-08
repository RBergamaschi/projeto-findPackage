from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.driver_profile_service import DriverProfileService
from app.schemas.driver_profile_schema import DriverProfileCreate, DriverProfileRead, DriverProfileUpdate, DriverProfileSummary
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse
from app.models.enums import UserRole, VehicleType
from app.auth.dependencies import require_admin, require_admin_or_driver
from app.core.exceptions import ForbiddenException
from app.models.user import User


router = APIRouter(prefix="/api/v1/driver-profiles", tags=["Driver Profiles Center"])

@router.get(
    "/",
    response_model=PaginatedResponse[DriverProfileSummary],
    status_code=status.HTTP_200_OK,
    summary="Get all driver profiles",
    description="Retrieve a paginated list of all driver profiles in the system.",
    responses={
        200: {"description": "List of driver profiles retrieved successfully."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_driver_profiles(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    params = PaginationParams(page=page, size=size)
    driver_profile_service = DriverProfileService(db)
    return await driver_profile_service.get_all_driver_profiles(params)

@router.get(
    "/{profile_id}",
    response_model=DriverProfileRead,
    status_code=status.HTTP_200_OK,
    summary="Get driver profile by ID",
    description="Retrieve a driver profile by its unique ID.",
    responses={
        200: {"description": "Driver profile retrieved successfully."},
        403: {"description": "Forbidden."},
        404: {"description": "Driver profile not found."},
        500: {"description": "Internal server error."}
    }
)
async def get_driver_profile_by_id(
    profile_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    driver_profile_service = DriverProfileService(db)
    return await driver_profile_service.get_driver_profile_by_id(profile_id)

@router.get(
    "/get-by-vehicle-type/{vehicle_type}",
    response_model=PaginatedResponse[DriverProfileSummary],
    status_code=status.HTTP_200_OK,
    summary="Get driver profiles by vehicle type",
    description="Retrieve a paginated list of driver profiles filtered by vehicle type.",
    responses={
        200: {"description": "List of driver profiles retrieved successfully."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_driver_profiles_by_vehicle_type(
    vehicle_type: VehicleType,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    params = PaginationParams(page=page, size=size)
    driver_profile_service = DriverProfileService(db)
    return await driver_profile_service.get_driver_profiles_by_vehicle_type(vehicle_type, params)

@router.get(
    "/get-by-availability/{is_available}",
    response_model=PaginatedResponse[DriverProfileSummary],
    status_code=status.HTTP_200_OK,
    summary="Get driver profiles by availability",
    description="Retrieve a paginated list of driver profiles filtered by availability status.",
    responses={
        200: {"description": "List of driver profiles retrieved successfully."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_driver_profiles_by_availability(
    is_available: bool,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    params = PaginationParams(page=page, size=size)
    driver_profile_service = DriverProfileService(db)
    return await driver_profile_service.get_driver_profiles_by_availability(is_available, params)

@router.post(
    "/",
    response_model=DriverProfileRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new driver profile",
    description="Create a new driver profile with the provided information.",
    responses={
        201: {"description": "Driver profile created successfully."},
        400: {"description": "Bad request."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def create_driver_profile(
    profile_data: DriverProfileCreate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    driver_profile_service = DriverProfileService(db)
    return await driver_profile_service.create_driver_profile(profile_data)

@router.put(
    "/{profile_id}",
    response_model=DriverProfileRead,
    status_code=status.HTTP_200_OK,
    summary="Update a driver profile",
    description="Update an existing driver profile with the provided information.",
    responses={
        200: {"description": "Driver profile updated successfully."},
        400: {"description": "Bad request."},
        403: {"description": "Forbidden."},
        404: {"description": "Driver profile not found."},
        500: {"description": "Internal server error."}
    }
)
async def update_driver_profile(
    profile_id: int,
    profile_data: DriverProfileUpdate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    if current_user.user_role != UserRole.ADMIN:
        if not current_user.driver_profile or current_user.driver_profile.id != profile_id:
            raise ForbiddenException("You do not have permission to update this driver profile.")
    driver_profile_service = DriverProfileService(db)
    return await driver_profile_service.update_driver_profile(profile_id, profile_data)

@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a driver profile",
    description="Delete an existing driver profile by its unique ID.",
    responses={
        204: {"description": "Driver profile deleted successfully."},
        403: {"description": "Forbidden."},
        404: {"description": "Driver profile not found."},
        500: {"description": "Internal server error."}
    }
)
async def delete_driver_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    driver_profile_service = DriverProfileService(db)
    await driver_profile_service.delete_driver_profile(profile_id)