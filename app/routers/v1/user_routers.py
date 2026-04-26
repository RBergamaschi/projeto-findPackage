from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.configs.database import get_db_connection
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead


router = APIRouter(prefix="/users", tags=["User Center"])

@router.get(
    "/",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
    description="Retrieve a list of all users in the system.",
    responses={
        200: {"description": "List of users retrieved successfully."},
        500: {"description": "Internal server error."}
    }
)
async def get_all_users(
    db: AsyncSession = Depends(get_db_connection)
):
    user_service = UserService(db)
    return await user_service.get_all_users()

@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get User by ID",
    description="Retrieve a user by their unique ID.",
    responses={
        200: {"description": "User retrieved successfully."},
        404: {"description": "User not found."},
        500: {"description": "Internal server error."}
    }
)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)

@router.get(
    "/get-by-email/{email}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get User by Email",
    description="Retrieve a user by their email address.",
    responses={
        200: {"description": "User retrieved successfully."},
        404: {"description": "User not found."},
        500: {"description": "Internal server error."}
    }
)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db_connection)
):
    user_service = UserService(db)
    return await user_service.get_user_by_email(email)

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create User with Address",
    description="Create a new user along with their address information.",
    responses={
        201: {"description": "User created successfully."},
        409: {"description": "Email already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_user_with_address(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db_connection)
):
    user_service = UserService(db)
    return await user_service.create_user_with_address(user_create)

@router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update User",
    description="Update an existing user's information.",
    responses={
        200: {"description": "User updated successfully."},
        404: {"description": "User not found."},
        500: {"description": "Internal server error."}
    }
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db_connection)
):
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_update)

@router.delete(
    "/{user_id}",
    summary="Delete User",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a user by their unique ID.",
    responses={
        204: {"description": "User deleted successfully."},
        404: {"description": "User not found."},
        500: {"description": "Internal server error."}
    }
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    user_service = UserService(db)
    return await user_service.delete_user(user_id)