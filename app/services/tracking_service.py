from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tracking import Tracking
from app.repositories.tracking_repository import TrackingRepository
from app.schemas.tracking_schema import TrackingCreate, TrackingRead
from app.core.exceptions import NotFoundException
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse


class TrackingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tracking_repository = TrackingRepository(db)
    
    async def get_tracking_by_id(self, tracking_id: int) -> TrackingRead:
        tracking = await self.tracking_repository.get_by_id(tracking_id)
        if not tracking:
            raise NotFoundException("Tracking not found")
        return TrackingRead.model_validate(tracking)
    
    async def get_tracking_by_order_id(self, order_id: int, params: PaginationParams) -> PaginatedResponse[TrackingRead]:
        offset = (params.page - 1) * params.size
        tracking_list, total = await self.tracking_repository.get_by_order_id(order_id, limit=params.size, offset=offset)
        if not total:
            raise NotFoundException("No tracking found for the given order ID")
        pages = -(-total // params.size)

        return PaginatedResponse(
            items=[TrackingRead.model_validate(tracking) for tracking in tracking_list],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

    async def get_latest_tracking_by_order_id(self, order_id: int)-> TrackingRead:
        tracking = await self.tracking_repository.get_latest_by_order_id(order_id)
        if not tracking:
            raise NotFoundException("Tracking not found")
        return TrackingRead.model_validate(tracking)
    
    async def get_all_tracking(self, params: PaginationParams) -> PaginatedResponse[TrackingRead]:
        offset = (params.page - 1) * params.size
        tracking_list, total = await self.tracking_repository.get_all(limit=params.size, offset=offset)
        pages = -(-total // params.size)
        
        return PaginatedResponse(
            items=[TrackingRead.model_validate(tracking) for tracking in tracking_list],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def create_tracking(self, tracking_create: TrackingCreate) -> TrackingRead:
        tracking = Tracking(**tracking_create.model_dump())
        created_tracking = await self.tracking_repository.create(tracking)
        await self.db.commit()
        return TrackingRead.model_validate(created_tracking)