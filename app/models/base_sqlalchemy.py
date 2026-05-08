from app.models.base_model import EntityMeta as Base
from app.configs.database import Engine


async def init_db():
    from app.models import(
        user,
        address,
        order,
        tracking,
        driver_profile
    )
    
    async with Engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)