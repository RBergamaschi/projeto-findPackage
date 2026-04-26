from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderRead
from app.models.enums import OrderStatus
from app.core.exceptions import NotFoundException


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repository = OrderRepository(db)
    
    async def get_order_by_id(self, order_id: int) -> OrderRead:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        return OrderRead.model_validate(order)
    
    async def get_orders_by_status(self, status: OrderStatus) -> list[OrderRead]:
        orders = await self.order_repository.get_by_status(status)
        return [OrderRead.model_validate(order) for order in orders]
    
    async def get_orders_by_user_id(self, user_id: int) -> list[OrderRead]:
        orders = await self.order_repository.get_by_user_id(user_id)
        return [OrderRead.model_validate(order) for order in orders]
    
    async def get_all_orders(self) -> list[OrderRead]:
        orders = await self.order_repository.get_all()
        return [OrderRead.model_validate(order) for order in orders]
    
    async def create_order(self, order_create: OrderCreate) -> OrderRead:
        order = Order(**order_create.model_dump())
        created_order = await self.order_repository.create(order)
        return OrderRead.model_validate(created_order)
    
    async def update_order(self, order_id: int, order_update: OrderUpdate) -> OrderRead:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        
        for field, value in order_update.model_dump(exclude_unset=True).items():
            setattr(order, field, value)
        
        updated_order = await self.order_repository.update(order)
        return OrderRead.model_validate(updated_order)
    
    async def delete_order(self, order_id: int) -> None:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        await self.order_repository.delete(order)