from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.repositories.address_repository import AddressRepository
from app.schemas.address_schema import AddressUpdate, AddressRead
from app.core.exceptions import NotFoundException
from app.schemas.pagination_schema import PaginationParams, PaginatedResponse


class AddressService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.address_repository = AddressRepository(db)
    
    async def get_address_by_id(self, address_id: int) -> AddressRead:
        address = await self.address_repository.get_by_id(address_id)
        if not address:
            raise NotFoundException("Address not found")
        return AddressRead.model_validate(address)
    
    async def get_addresses_by_cep(self, cep: str, params: PaginationParams) -> PaginatedResponse[AddressRead]:
        offset = (params.page - 1) * params.size
        addresses, total = await self.address_repository.get_by_cep(cep, limit=params.size, offset=offset)
        if not total:
            raise NotFoundException("No addresses found for the given CEP")
        pages = -(-total // params.size)

        return PaginatedResponse(
            items=[AddressRead.model_validate(address) for address in addresses],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

    async def get_all_addresses(self, params: PaginationParams) -> PaginatedResponse[AddressRead]:
        offset = (params.page - 1) * params.size
        addresses, total = await self.address_repository.get_all(limit=params.size, offset=offset)
        pages = -(-total // params.size)

        return PaginatedResponse(
            items=[AddressRead.model_validate(address) for address in addresses],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

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