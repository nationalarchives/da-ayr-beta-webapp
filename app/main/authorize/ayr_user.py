from typing import List

from sqlalchemy import exc

from app.main.authorize.keycloak_manager import (
    get_user_transferring_body_keycloak_groups,
)
from app.main.db.models import Body, db


class AYRUser:
    def __init__(self, groups: List[str]) -> None:
        self.groups = groups

    @property
    def can_access_ayr(self):
        return self.is_superuser or self.is_standard_user

    @property
    def is_superuser(self) -> bool:
        return "/ayr_user_type/view_all" in self.groups

    @property
    def is_standard_user(self) -> bool:
        return "/ayr_user_type/view_dept" in self.groups

    @property
    def transferring_body(self) -> str | None:
        if self.is_superuser or not self.is_standard_user:
            return None

        user_accessible_transferring_bodies = (
            get_user_accessible_transferring_bodies(self.groups)
        )
        if not user_accessible_transferring_bodies:
            return None

        user_transferring_body = user_accessible_transferring_bodies[0]
        return user_transferring_body


def get_user_accessible_transferring_bodies(groups: List[str]) -> List[str]:
    user_transferring_bodies = get_user_transferring_body_keycloak_groups(
        groups
    )

    if not user_transferring_bodies:
        return []

    try:
        query = db.session.query(Body.Name)
        bodies = db.session.execute(query)
    except exc.SQLAlchemyError as e:
        print("Failed to return results from database with error : " + str(e))
        return []

    user_accessible_transferring_bodies = []

    for body in bodies:
        body_name = body.Name
        if _body_in_users_groups(body_name, user_transferring_bodies):
            user_accessible_transferring_bodies.append(body_name)

    return user_accessible_transferring_bodies


def _body_in_users_groups(body, user_transferring_body_keycloak_groups):
    for user_group in user_transferring_body_keycloak_groups:
        if (
            user_group.strip().replace(" ", "").lower()
            == body.strip().replace(" ", "").lower()
        ):
            return True

    return False
