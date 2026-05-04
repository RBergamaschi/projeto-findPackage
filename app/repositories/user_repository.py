from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.address))
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.email == email)
            .options(selectinload(User.address))
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, limit: int, offset: int) -> tuple[list[User], int]:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.address))
            .limit(limit)
            .offset(offset)
        )
        users = result.scalars().all()
        
        count_result = await self.db.execute(
            select(func.count()).select_from(User)
        )
        total = count_result.scalar()
        
        return users, total
    
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.flush()