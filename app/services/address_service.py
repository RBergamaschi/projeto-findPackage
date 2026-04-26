from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.repositories.address_repository import AddressRepository
from app.schemas.address_schema import AddressUpdate, AddressRead
from app.core.exceptions import NotFoundException


class AddressService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.address_repository = AddressRepository(db)
    
    async def get_address_by_id(self, address_id: int) -> AddressRead:
        address = await self.address_repository.get_by_id(address_id)
        if not address:
            raise NotFoundException("Address not found")
        return AddressRead.model_validate(address)
    
    async def get_addresses_by_cep(self, cep: str) -> list[AddressRead]:
        addresses = await self.address_repository.get_by_cep(cep)
        return [AddressRead.model_validate(address) for address in addresses]
    
    async def get_all_addresses(self) -> list[AddressRead]:
        addresses = await self.address_repository.get_all()
        return [AddressRead.model_validate(address) for address in addresses]
    
    async def update_address(self, address_id: int, address_update: AddressUpdate) -> AddressRead:
        address = await self.address_repository.get_by_id(address_id)
        if not address:
            raise NotFoundException("Address not found")
        
        data = address_update.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(address, key, value)
        
        address = await self.address_repository.update(address)
        await self.db.commit()
        return AddressRead.model_validate(address)