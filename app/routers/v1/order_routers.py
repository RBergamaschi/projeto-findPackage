from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_db_connection
from app.services.order_service import OrderService
from app.schemas.order_schema import OrderCreate, OrderRead, OrderUpdate
from app.models.enums import OrderStatus


router = APIRouter(prefix="/orders", tags=["Orders Center"])

@router.get(
    "/",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get all orders",
    description="Retrieve a list of all orders in the system.",
    responses={
        200: {"description": "List of orders retrieved successfully."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_orders(
    db: AsyncSession = Depends(get_db_connection)
):
    order_service = OrderService(db)
    return await order_service.get_all_orders()

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
    db: AsyncSession = Depends(get_db_connection)
):
    order_service = OrderService(db)
    return await order_service.get_order_by_id(order_id)

@router.get(
    "/get-by-status/{status}",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get orders by status",
    description="Retrieve a list of orders by their status.",
    responses={
        200: {"description": "Orders retrieved successfully."},
        500: {"description": "Internal server error."}
    }
)
async def get_orders_by_status(
    status: OrderStatus,
    db: AsyncSession = Depends(get_db_connection)
):
    order_service = OrderService(db)
    return await order_service.get_orders_by_status(status)

@router.get(
    "/get-by-user/{user_id}",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get orders by user ID",
    description="Retrieve a list of orders by the user ID.",
    responses={
        200: {"description": "Orders retrieved successfully."},
        500: {"description": "Internal server error."}
    }
)
async def get_orders_by_user_id(
    user_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    order_service = OrderService(db)
    return await order_service.get_orders_by_user_id(user_id)

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
    db: AsyncSession = Depends(get_db_connection)
):
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
        400: {"description": "Invalid order data."},
        404: {"description": "Order not found."},
        500: {"description": "Internal server error."}
    }
)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: AsyncSession = Depends(get_db_connection)
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
        404: {"description": "Order not found."},
        500: {"description": "Internal server error."}
    }
)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    order_service = OrderService(db)
    await order_service.delete_order(order_id)