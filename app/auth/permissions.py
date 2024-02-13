from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT


class PermissionChecker:
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, Authorize: AuthJWT = Depends()) -> bool:
        """
        Checks if the current user has the required permissions.

        This method is called automatically by FastAPI when a route handler declares
        a PermissionChecker dependency.

        Parameters:
            Authorize (AuthJWT): The AuthJWT dependency to access the JWT token.

        Raises:
            HTTPException: 403 Forbidden if the user does not have the required permissions.

        Returns:
            bool: True if the user has all required permissions, otherwise raises an exception.
        """
        Authorize.jwt_required()
        token = Authorize.get_raw_jwt()
        user_permissions = token.get("permissions", [])

        for r_perm in self.required_permissions:
            if r_perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
        return True
