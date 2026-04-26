from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
    
    async def get_by_status(self, status: OrderStatus) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .where(Order.status == status)
            .options(selectinload(Order.user), selectinload(Order.address))
        )
        return result.scalars().all()
    
    async def get_by_user_id(self, user_id: int) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.user), selectinload(Order.address))
        )
        return result.scalars().all()
    
    async def get_all(self) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.user), selectinload(Order.address))
        )
        return result.scalars().all()
    
    async def create(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def update(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def delete(self, order: Order) -> None:
        await self.db.delete(order)
        await self.db.commit()