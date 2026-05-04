from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.tracking_service import TrackingService
from app.schemas.tracking_schema import TrackingRead, TrackingCreate
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse
from app.auth.jwt_handler import get_current_user
from app.auth.dependencies import require_admin, require_admin_or_driver
from app.models.user import User


router = APIRouter(prefix="/api/v1/tracking", tags=["Tracking Center"])

@router.get(
    "/",
    response_model=PaginatedResponse[TrackingRead],
    status_code=status.HTTP_200_OK,
    summary="Get all tracking records",
    description="Retrieve a paginated list of all tracking records in the system.",
    responses={
        200: {"description": "A list of tracking records."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_tracking(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    params = PaginationParams(page=page, size=size)
    tracking_service = TrackingService(db)
    return await tracking_service.get_all_tracking(params)

@router.get(
    "/{tracking_id}",
    response_model=TrackingRead,
    status_code=status.HTTP_200_OK,
    summary="Get tracking by ID",
    description="Retrieve a tracking record by its unique ID.",
    responses={
        200: {"description": "The tracking record."},
        404: {"description": "Tracking not found."},
        500: {"description": "Internal server error."}
    }
)
async def get_tracking_by_id(
    tracking_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    tracking_service = TrackingService(db)
    return await tracking_service.get_tracking_by_id(tracking_id)

@router.get(
    "/get-by-order/{order_id}",
    response_model=PaginatedResponse[TrackingRead],
    status_code=status.HTTP_200_OK,
    summary="Get tracking by Order ID",
    description="Retrieve a paginated list of tracking records for a specific order.",
    responses={
        200: {"description": "A list of tracking records for the specified order."},
        404: {"description": "No tracking records found for the specified order."},
        500: {"description": "Internal server error."}
    }
)
async def get_tracking_by_order_id(
    order_id: int,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, size=size)
    tracking_service = TrackingService(db)
    return await tracking_service.get_tracking_by_order_id(order_id, params)

@router.get(
    "/get-latest-by-order/{order_id}",
    response_model=TrackingRead,
    status_code=status.HTTP_200_OK,
    summary="Get latest tracking by Order ID",
    description="Retrieve the latest tracking record associated with a specific order ID.",
    responses={
        200: {"description": "The latest tracking record for the specified order."},
        404: {"description": "No tracking records found for the specified order."},
        500: {"description": "Internal server error."}
    }
)
async def get_latest_tracking_by_order_id(
    order_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_user)
):
    tracking_service = TrackingService(db)
    return await tracking_service.get_latest_tracking_by_order_id(order_id)

@router.post(
    "/",
    response_model=TrackingRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tracking record",
    description="Create a new tracking record for an order.",
    responses={
        201: {"description": "The created tracking record."},
        400: {"description": "Invalid input data."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def create_tracking(
    tracking_create: TrackingCreate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    tracking_service = TrackingService(db)
    return await tracking_service.create_tracking(tracking_create)
