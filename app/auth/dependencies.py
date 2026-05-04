from fastapi import Depends

from app.auth.jwt_handler import get_current_user
from app.core.exceptions import ForbiddenException
from app.models.user import User
from app.models.enums import UserRole


def require_roles(*roles: UserRole):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.user_role not in roles:
            raise ForbiddenException("You do not have permission to access this resource.")
        return current_user
    return dependency


require_admin = require_roles(UserRole.ADMIN)
require_driver = require_roles(UserRole.DRIVER)
require_admin_or_driver = require_roles(UserRole.ADMIN, UserRole.DRIVER)