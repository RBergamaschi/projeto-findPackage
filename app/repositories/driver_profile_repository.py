from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.driver_profile import DriverProfile
from app.models.user import User
from app.models.enums import VehicleType


class DriverProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, profile_id: int) -> DriverProfile | None:
        result = await self.db.execute(
            select(DriverProfile)
            .where(DriverProfile.id == profile_id)
            .options(selectinload(DriverProfile.user))
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, limit: int, offset: int) -> tuple[list[DriverProfile], int]:
        result = await self.db.execute(
            select(DriverProfile)
            .options(selectinload(DriverProfile.user))
            .limit(limit)
            .offset(offset)
        )
        profiles = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(DriverProfile)
        )
        total = count_result.scalar()
        
        return profiles, total
    
    async def get_by_vehicle_type(self, vehicle_type: VehicleType, limit: int, offset: int) -> tuple[list[DriverProfile], int]:
        result = await self.db.execute(
            select(DriverProfile)
            .where(DriverProfile.vehicle_type == vehicle_type)
            .options(selectinload(DriverProfile.user))
            .limit(limit)
            .offset(offset)
        )
        drivers = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count(DriverProfile.id))
            .where(DriverProfile.vehicle_type == vehicle_type)
        )
        total = count_result.scalar()
        
        return drivers, total
    async def get_by_availability(self, is_available: bool, limit: int, offset: int) -> tuple[list[DriverProfile], int]:
        result = await self.db.execute(
            select(DriverProfile)
            .where(DriverProfile.is_available == is_available)
            .options(selectinload(DriverProfile.user))
            .limit(limit)
            .offset(offset)
        )
        drivers = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count(DriverProfile.id))
            .where(DriverProfile.is_available == is_available)
        )
        total = count_result.scalar()
        
        return drivers, total
    
    async def create(self, driver: DriverProfile) -> DriverProfile:
        self.db.add(driver)
        await self.db.flush()
        await self.db.refresh(driver)
        return driver
    
    async def update(self, driver: DriverProfile) -> DriverProfile:
        self.db.add(driver)
        await self.db.flush()
        await self.db.refresh(driver)
        return driver
    
    async def delete(self, driver: DriverProfile) -> None:
        await self.db.delete(driver)
        await self.db.flush()