import json
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError

from app.configs.environment import get_environment_settings
from app.auth.security import hash_password
from app.models.user import User
from app.models.address import Address


env = get_environment_settings()
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "assets"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


async def seed_users_base(db: AsyncSession):
    users_data = load_json(DATA_DIR / "users.json")

    for user in users_data:
        # Passo 1: verifica se o usuário já existe pelo email
        result = await db.execute(select(User).where(User.email == user["email"]))
        if result.scalar_one_or_none():
            continue

        # Passo 2: cria o objeto Address a partir do bloco "address" do JSON
        address_data = user.get("address")
        address_obj = None
        if address_data:
            address_obj = Address(
                cep=address_data["cep"],
                state=address_data["state"],
                city=address_data["city"],
                neighborhood=address_data["neighborhood"],
                street=address_data["street"],
                number=address_data["number"],
                complement=address_data.get("complement"),
            )

        # Passo 3: cria o User e vincula o address — o SQLAlchemy preenche address_id sozinho
        new_user = User(
            first_name=user["first_name"],
            last_name=user["last_name"],
            social_name=user.get("social_name"),
            email=user["email"],
            hashed_password=hash_password(user["password"]),
            address=address_obj,
        )

        # Passo 4: adiciona na sessão e salva
        try:
            db.add(new_user)
            await db.commit()
        except IntegrityError:
            await db.rollback()

async def run_seed(db: AsyncSession):
    tarefa = [
        ("users", seed_users_base),
    ]
    
    for nome, func_seed in tarefa:
        try:
            print(f"Seeding {nome}...")
            await func_seed(db)
        except Exception as e:
            print(f"Error seeding {nome}: {e}")
            await db.rollback()
    print("Seeding completed.")