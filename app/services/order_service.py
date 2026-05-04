from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderRead
from app.models.enums import OrderStatus
from app.core.exceptions import NotFoundException
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repository = OrderRepository(db)
    
    async def get_order_by_id(self, order_id: int) -> OrderRead:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        return OrderRead.model_validate(order)
    
    async def get_orders_by_status(self, status: OrderStatus, params: PaginationParams) -> PaginatedResponse[OrderRead]:
        offset = (params.page - 1) * params.size
        orders, total = await self.order_repository.get_by_status(status, limit=params.size, offset=offset)
        pages = -(-total // params.size)
        
        return PaginatedResponse(
            items=[OrderRead.model_validate(order) for order in orders],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def get_orders_by_status_and_user_id(self, status: OrderStatus, user_id: int, params: PaginationParams) -> PaginatedResponse[OrderRead]:
        offset = (params.page - 1) * params.size
        orders, total = await self.order_repository.get_by_status_and_user_id(status, user_id, limit=params.size, offset=offset)
        pages = -(-total // params.size)
        
        return PaginatedResponse(
            items=[OrderRead.model_validate(order) for order in orders],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def get_orders_by_user_id(self, user_id: int, params: PaginationParams) -> PaginatedResponse[OrderRead]:
        offset = (params.page - 1) * params.size
        orders, total = await self.order_repository.get_by_user_id(user_id, limit=params.size, offset=offset)
        if not total:
            raise NotFoundException("No orders found for the given user ID")
        pages = -(-total // params.size)

        return PaginatedResponse(
            items=[OrderRead.model_validate(order) for order in orders],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def get_all_orders(self, params: PaginationParams) -> PaginatedResponse[OrderRead]:
        offset = (params.page - 1) * params.size
        orders, total = await self.order_repository.get_all(limit=params.size, offset=offset)
        pages = -(-total // params.size)

        return PaginatedResponse(
            items=[OrderRead.model_validate(order) for order in orders],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

    async def create_order(self, order_create: OrderCreate) -> OrderRead:
        order = Order(**order_create.model_dump())
        created_order = await self.order_repository.create(order)
        await self.db.commit()
        return OrderRead.model_validate(created_order)
    
    async def update_order(self, order_id: int, order_update: OrderUpdate) -> OrderRead:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        
        for field, value in order_update.model_dump(exclude_unset=True).items():
            setattr(order, field, value)
        
        updated_order = await self.order_repository.update(order)
        await self.db.commit()
        return OrderRead.model_validate(updated_order)
    
    async def delete_order(self, order_id: int) -> None:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        await self.order_repository.delete(order)
        await self.db.commit()