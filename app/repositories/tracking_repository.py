from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.tracking import Tracking


class TrackingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, tracking_id: int) -> Tracking | None:
        result = await self.db.execute(
            select(Tracking)
            .where(Tracking.id == tracking_id)
            .options(selectinload(Tracking.order))
        )
        return result.scalar_one_or_none()
    
    async def get_by_order_id(self, order_id: int) -> list[Tracking]:
        result = await self.db.execute(
            select(Tracking)
            .where(Tracking.order_id == order_id)
            .options(selectinload(Tracking.order))
        )
        return result.scalars().all()
    
    async def get_latest_by_order_id(self, order_id: int) -> Tracking | None:
        result = await self.db.execute(
            select(Tracking)
            .where(Tracking.order_id == order_id)
            .order_by(Tracking.sent_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[Tracking]:
        result = await self.db.execute(
            select(Tracking)
            .options(selectinload(Tracking.order))
        )
        return result.scalars().all()
    
    async def create(self, tracking: Tracking) -> Tracking:
        self.db.add(tracking)
        await self.db.commit()
        await self.db.refresh(tracking)
        return tracking