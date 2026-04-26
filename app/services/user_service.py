from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.address_repository import AddressRepository
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead, UserSummary
from app.auth.security import hash_password
from app.core.exceptions import NotFoundException, ConflictException


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)
        self.address_repository = AddressRepository(db)
    
    async def get_user_by_id(self, user_id: int) -> UserRead:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserRead.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserRead:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise NotFoundException("User not found")
        return UserRead.model_validate(user)

    async def get_all_users(self) -> list[UserRead]:
        users = await self.user_repository.get_all()
        return [UserRead.model_validate(user) for user in users]
    
    async def create_user_with_address(self, user_create: UserCreate) -> UserRead:
        if await self.user_repository.get_by_email(user_create.email):
            raise ConflictException("Email already exists")
        
        address = Address(**user_create.address.model_dump())
        address = await self.address_repository.create(address)
        
        hashed_password = hash_password(user_create.password)
        user = User(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            social_name=user_create.social_name,
            email=user_create.email,
            hashed_password=hashed_password,
            address_id=address.id
        )
        
        user = await self.user_repository.create(user)
        await self.db.commit()
        return UserRead.model_validate(user)
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserRead:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        data = user_update.model_dump(exclude_unset=True)
        
        if "password" in data:
            data["hashed_password"] = hash_password(data.pop("password"))
        
        for field, value in data.items():
            setattr(user, field, value)
        
        user = await self.user_repository.update(user)
        await self.db.commit()
        return UserRead.model_validate(user)
    
    async def delete_user(self, user_id: int)-> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        await self.user_repository.delete(user)
        await self.db.commit()