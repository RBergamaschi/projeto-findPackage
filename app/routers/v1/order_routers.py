from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.order_service import OrderService
from app.schemas.order_schema import OrderCreate, OrderRead, OrderUpdate
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse
from app.models.enums import OrderStatus, UserRole
from app.auth.jwt_handler import get_current_user
from app.auth.dependencies import require_admin, require_admin_or_driver
from app.core.exceptions import ForbiddenException
from app.models.user import User


router = APIRouter(prefix="/api/v1/orders", tags=["Orders Center"])

@router.get(
    "/",
    response_model=PaginatedResponse[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get all orders",
    description="Retrieve a paginated list of all orders in the system.",
    responses={
        200: {"description": "List of orders retrieved successfully."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_orders(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    params = PaginationParams(page=page, size=size)
    order_service = OrderService(db)
    return await order_service.get_all_orders(params)

@router.get(
    "/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    summary="Get order by ID",
    description="Retrieve an order by its unique ID.",
    responses={
        200: {"description": "Order retrieved successfully."},
        404: {"description": "Order not found."},
        500: {"description": "Internal server error."}
    }
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    order_service = OrderService(db)
    return await order_service.get_order_by_id(order_id)

@router.get(
    "/get-by-status/{order_status}",
    response_model=PaginatedResponse[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get orders by status",
    description="Retrieve a paginated list of orders by their status.",
    responses={
        200: {"description": "Orders retrieved successfully."},
        403: {"description": "Forbidden."},
        500: {"description": "Internal server error."}
    }
)
async def get_orders_by_status(
    order_status: OrderStatus,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_user) 
):
    params = PaginationParams(page=page, size=size)
    order_service = OrderService(db)
    
    if current_user.user_role == UserRole.CUSTOMER:
        return await order_service.get_orders_by_status_and_user_id(order_status, current_user.id, params)
    
    return await order_service.get_orders_by_status(order_status, params)

@router.get(
    "/get-by-user/{user_id}",
    response_model=PaginatedResponse[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get orders by user ID",
    description="Retrieve a paginated list of orders by the user ID.",
    responses={
        200: {"description": "Orders retrieved successfully."},
        404: {"description": "No orders found for the given user."},
        500: {"description": "Internal server error."}
    }
)
async def get_orders_by_user_id(
    user_id: int,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_role == UserRole.DRIVER:
        raise ForbiddenException("Drivers do not have permission to view orders for specific users.")
    
    if current_user.user_role == UserRole.CUSTOMER and current_user.id != user_id:
        raise ForbiddenException("You do not have permission to view orders for this user.")
    
    params = PaginationParams(page=page, size=size)
    order_service = OrderService(db)
    return await order_service.get_orders_by_user_id(user_id, params)

@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    description="Create a new order in the system.",
    responses={
        201: {"description": "Order created successfully."},
        400: {"description": "Invalid order data."},
        500: {"description": "Internal server error."}
    }
)
async def create_order(
    order_create: OrderCreate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_role == UserRole.DRIVER:
        raise ForbiddenException("Drivers do not have permission to create orders.")
    
    order_create.user_id = current_user.id
    order_service = OrderService(db)
    return await order_service.create_order(order_create)

@router.put(
    "/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    summary="Update an existing order",
    description="Update an existing order by its unique ID.",
    responses={
        200: {"description": "Order updated successfully."},
        403: {"description": "Forbidden."},
        404: {"description": "Order not found."},
        500: {"description": "Internal server error."}
    }
)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin_or_driver)
):
    order_service = OrderService(db)
    return await order_service.update_order(order_id, order_update)

@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an order",
    description="Delete an existing order by its unique ID.",
    responses={
        204: {"description": "Order deleted successfully."},
        403: {"description": "Forbidden."},
        404: {"description": "Order not found."},
        500: {"description": "Internal server error."}
    }
)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin)
):
    order_service = OrderService(db)
    await order_service.delete_order(order_id)
