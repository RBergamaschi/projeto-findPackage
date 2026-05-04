from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth.jwt_handler import (
    create_access_token,
    authenticate_user,
    get_current_user
)
from app.configs.database import get_db_connection
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, Token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.schemas.user_schema import UserRead


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication Center"])
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user and return an access token.",
    responses={
        200: {"description": "Authentication successful, access token returned."},
        401: {"description": "Invalid email or password."},
        500: {"description": "Internal server error."}
    }
)
@limiter.limit("5/minute")
async def token(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db_connection)
):
    user = await authenticate_user(
        login_data.email,
        login_data.password,
        db
    )
    if not user:
        raise UnauthorizedException("Invalid email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post(
    "/refresh-token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="Refresh the access token for an authenticated user.",
    responses={
        200: {"description": "Access token refreshed successfully."},
        401: {"description": "Invalid or expired token."},
        500: {"description": "Internal server error."}
    }
)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    access_token = create_access_token(data={"sub": str(current_user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get Current User",
    description="Retrieve the currently authenticated user's information.",
    responses={
        200: {"description": "Current user information retrieved successfully."},
        401: {"description": "Invalid or expired token."},
        500: {"description": "Internal server error."}
    }
)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return UserRead.model_validate(current_user)