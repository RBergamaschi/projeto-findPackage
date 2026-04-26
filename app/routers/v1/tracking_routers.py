from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.tracking_service import TrackingService
from app.schemas.tracking_schema import TrackingRead, TrackingCreate


router = APIRouter(prefix="/tracking", tags=["Tracking Center"])

@router.get(
    "/",
    response_model=list[TrackingRead],
    status_code=status.HTTP_200_OK,
    summary="Get all tracking records",
    description="Retrieve a list of all tracking records in the system.",
    responses={
        200: {"description": "A list of tracking records."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_tracking(
    db: AsyncSession = Depends(get_db_connection)
):
    tracking_service = TrackingService(db)
    return await tracking_service.get_all_tracking()

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
    db: AsyncSession = Depends(get_db_connection)
):
    tracking_service = TrackingService(db)
    return await tracking_service.get_tracking_by_id(tracking_id)

@router.get(
    "/get-by-order/{order_id}",
    response_model=list[TrackingRead],
    status_code=status.HTTP_200_OK,
    summary="Get tracking by Order ID",
    description="Retrieve tracking records associated with a specific order ID.",
    responses={
        200: {"description": "A list of tracking records for the specified order."},
        404: {"description": "No tracking records found for the specified order."},
        500: {"description": "Internal server error."}
    }
)
async def get_tracking_by_order_id(
    order_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    tracking_service = TrackingService(db)
    return await tracking_service.get_tracking_by_order_id(order_id)

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
    db: AsyncSession = Depends(get_db_connection)
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
        500: {"description": "Internal server error."}
    }
)
async def create_tracking(
    tracking_create: TrackingCreate,
    db: AsyncSession = Depends(get_db_connection)
):
    tracking_service = TrackingService(db)
    return await tracking_service.create_tracking(tracking_create)