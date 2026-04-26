from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tracking import Tracking
from app.repositories.tracking_repository import TrackingRepository
from app.schemas.tracking_schema import TrackingCreate, TrackingRead
from app.core.exceptions import NotFoundException


class TrackingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tracking_repository = TrackingRepository(db)
    
    async def get_tracking_by_id(self, tracking_id: int) -> TrackingRead:
        tracking = await self.tracking_repository.get_by_id(tracking_id)
        if not tracking:
            raise NotFoundException("Tracking not found")
        return TrackingRead.model_validate(tracking)
    
    async def get_tracking_by_order_id(self, order_id: int) -> list[TrackingRead]:
        tracking_list = await self.tracking_repository.get_by_order_id(order_id)
        return [TrackingRead.model_validate(tracking) for tracking in tracking_list]
    
    async def get_latest_tracking_by_order_id(self, order_id: int)-> TrackingRead:
        tracking = await self.tracking_repository.get_latest_by_order_id(order_id)
        if not tracking:
            raise None
        return TrackingRead.model_validate(tracking)
    
    async def get_all_tracking(self) -> list[TrackingRead]:
        tracking_list = await self.tracking_repository.get_all()
        return [TrackingRead.model_validate(tracking) for tracking in tracking_list]
    
    async def create_tracking(self, tracking_create: TrackingCreate) -> TrackingRead:
        tracking = Tracking(**tracking_create.model_dump())
        created_tracking = await self.tracking_repository.create(tracking)
        return TrackingRead.model_validate(created_tracking)