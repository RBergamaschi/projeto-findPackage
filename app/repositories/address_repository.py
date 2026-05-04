from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.address import Address


class AddressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, address_id: int) -> Address | None:
        result = await self.db.execute(
            select(Address)
            .where(Address.id == address_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_cep(self, cep: str, limit: int, offset: int) -> tuple[list[Address], int]:
        result = await self.db.execute(
            select(Address)
            .where(Address.cep == cep)
            .limit(limit)
            .offset(offset)
        )
        addresses = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(Address).where(Address.cep == cep)
        )
        total = count_result.scalar()
        
        return addresses, total
    
    async def get_all(self, limit: int, offset: int) -> tuple[list[Address], int]:
        result = await self.db.execute(
            select(Address)
            .limit(limit)
            .offset(offset)
        )
        addresses = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(Address)
        )
        total = count_result.scalar()
        
        return addresses, total
    
    async def create(self, address: Address) -> Address:
        self.db.add(address)
        await self.db.flush()
        await self.db.refresh(address)
        return address
    
    async def update(self, address: Address) -> Address:
        self.db.add(address)
        await self.db.flush()
        await self.db.refresh(address)
        return address
    
    async def delete(self, address: Address) -> None:
        await self.db.delete(address)
        await self.db.flush()