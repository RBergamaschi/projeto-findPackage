from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.enums import OrderStatus
from app.models.order import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.user), selectinload(Order.address))
        )
        return result.scalar_one_or_none()
    
    async def get_by_status(self, status: OrderStatus, limit: int, offset: int) -> tuple[list[Order], int]:
        result = await self.db.execute(
            select(Order)
            .where(Order.status == status)
            .options(selectinload(Order.user), selectinload(Order.address))
            .limit(limit)
            .offset(offset)
        )
        orders = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(Order).where(Order.status == status)
        )
        total = count_result.scalar()
        
        return orders, total
    
    async def get_by_status_and_user_id(self, status: OrderStatus, user_id: int, limit: int, offset: int) -> tuple[list[Order], int]:
        result = await self.db.execute(
            select(Order)
            .where(Order.status == status, Order.user_id == user_id)
            .options(selectinload(Order.user), selectinload(Order.address))
            .limit(limit)
            .offset(offset)
        )
        orders = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(Order).where(Order.status == status, Order.user_id == user_id)
        )
        total = count_result.scalar()
        
        return orders, total
    
    async def get_by_user_id(self, user_id: int, limit: int, offset: int) -> tuple[list[Order], int]:
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.user), selectinload(Order.address))
            .limit(limit)
            .offset(offset)
        )
        orders = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(Order).where(Order.user_id == user_id)
        )
        total = count_result.scalar()
        
        return orders, total
    
    async def get_all(self, limit: int, offset: int) -> tuple[list[Order], int]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.user), selectinload(Order.address))
            .limit(limit)
            .offset(offset)
        )
        orders = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(Order)
        )
        total = count_result.scalar()
        
        return orders, total
    
    async def create(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)
        return order
    
    async def update(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)
        return order
    
    async def delete(self, order: Order) -> None:
        await self.db.delete(order)
        await self.db.flush()