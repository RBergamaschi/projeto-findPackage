from sqlalchemy.ext.asyncio import AsyncSession

from app.models.driver_profile import DriverProfile
from app.repositories.user_repository import UserRepository
from app.repositories.driver_profile_repository import DriverProfileRepository
from app.schemas.driver_profile_schema import DriverProfileCreate, DriverProfileRead, DriverProfileUpdate, DriverProfileSummary
from app.models.enums import VehicleType, UserRole
from app.core.exceptions import NotFoundException
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse


class DriverProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.driver_profile_repository = DriverProfileRepository(db)
        self.user_repository = UserRepository(db)
    
    async def get_driver_profile_by_id(self, profile_id: int) -> DriverProfileRead:
        profile = await self.driver_profile_repository.get_by_id(profile_id)
        if not profile:
            raise NotFoundException("Driver profile not found")
        return DriverProfileRead.model_validate(profile)
    
    async def get_all_driver_profiles(self, params: PaginationParams) -> PaginatedResponse[DriverProfileSummary]:
        offset = (params.page - 1) * params.size
        profiles, total = await self.driver_profile_repository.get_all(limit=params.size, offset=offset)
        pages = -(-total // params.size)
        
        return PaginatedResponse(
            items=[DriverProfileSummary.model_validate(profile) for profile in profiles],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def get_driver_profiles_by_vehicle_type(self, vehicle_type: VehicleType, params: PaginationParams) -> PaginatedResponse[DriverProfileSummary]:
        offset = (params.page - 1) * params.size
        profiles, total = await self.driver_profile_repository.get_by_vehicle_type(vehicle_type, limit=params.size, offset=offset)
        pages = -(-total // params.size)
        
        return PaginatedResponse(
            items=[DriverProfileSummary.model_validate(profile) for profile in profiles],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def get_driver_profiles_by_availability(self, is_available: bool, params: PaginationParams) -> PaginatedResponse[DriverProfileSummary]:
        offset = (params.page - 1) * params.size
        profiles, total = await self.driver_profile_repository.get_by_availability(is_available, limit=params.size, offset=offset)
        pages = -(-total // params.size)
        
        return PaginatedResponse(
            items=[DriverProfileSummary.model_validate(profile) for profile in profiles],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    async def create_driver_profile(self, profile_data: DriverProfileCreate) -> DriverProfileRead:
        user = await self.user_repository.get_by_id(profile_data.user_id)
        if not user:
            raise NotFoundException("User not found")
        
        if user.driver_profile:
            raise NotFoundException("This user already has a driver profile")
        
        profile = DriverProfile(**profile_data.model_dump().values())
        await self.driver_profile_repository.create(profile)
        
        user.user_role = UserRole.DRIVER
        await self.user_repository.update(user)
        
        await self.db.commit()
        return DriverProfileRead.model_validate(profile)
    
    async def update_driver_profile(self, profile_id: int, profile_data: DriverProfileUpdate) -> DriverProfileRead:
        existing_driver_profile = await self.driver_profile_repository.get_by_id(profile_id)
        if not existing_driver_profile:
            raise NotFoundException("Driver profile not found")
        
        for field, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(existing_driver_profile, field, value)
        
        updated_driver_profile = await self.driver_profile_repository.update(existing_driver_profile)
        await self.db.commit()
        return DriverProfileRead.model_validate(updated_driver_profile)
    
    async def delete_driver_profile(self, profile_id: int) -> None:
        existing_driver_profile = await self.driver_profile_repository.get_by_id(profile_id)
        if not existing_driver_profile:
            raise NotFoundException("Driver profile not found")
        
        user = existing_driver_profile.user
        user.user_role = UserRole.CUSTOMER
        await self.user_repository.update(user)
        
        await self.driver_profile_repository.delete(existing_driver_profile)
        await self.db.commit()