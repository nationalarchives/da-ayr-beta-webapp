from flask.testing import FlaskClient

from app.main.authorize.ayr_user import (
    AYRUser,
    get_user_accessible_transferring_bodies,
)
from app.tests.factories import BodyFactory


class TestAYRUser:
    def test_properties_when_ayr_user_type_view_dept_group(self):
        groups = ["/ayr_user_type/view_dept"]
        user = AYRUser(groups)
        assert user.can_access_ayr
        assert user.is_standard_user
        assert not user.is_superuser

    def test_properties_when_ayr_user_type_view_all_group(self):
        groups = ["/ayr_user_type/view_all"]
        user = AYRUser(groups)
        assert user.can_access_ayr
        assert user.is_superuser
        assert not user.is_standard_user

    def test_properties_when_no_valid_ayr_user_group(self):
        groups = ["/ayr_user_type/foo"]
        user = AYRUser(groups)
        assert not user.can_access_ayr
        assert not user.is_superuser
        assert not user.is_standard_user

    def test_when_transferring_body_user_prefix_in_groups(
        self, client, mock_standard_user
    ):
        BodyFactory(Name="foo")
        BodyFactory(Name="bar")
        mock_standard_user(client, ["foo", "bar"])
        groups = [
            "/ayr_user_type/view_dept",
            "/transferring_body_user/foo",
            "/transferring_body_user/bar",
        ]
        user = AYRUser(groups)
        assert user.transferring_bodies == ["foo", "bar"]

    def test_when_superuser_transferring_bodies_is_none(self):
        groups = ["/ayr_user_type/view_all", "/transferring_body_user/foo"]
        user = AYRUser(groups)
        assert user.transferring_bodies is None


class TestGetUserAccessibleTransferringBodies:
    def test_no_groups_returns_empty_list(
        self,
    ):
        """
        Given an empty list,
        When calling get_user_accessible_transferring_bodies with it
        Then it should return an empty list
        """
        results = get_user_accessible_transferring_bodies([])
        assert results == []

    def test_no_transferring_bodies_returns_empty_list(
        self,
    ):
        """
        Given a list of groups not containing any /transferring_body_user/ groups
        When I call get_user_accessible_transferring_bodies with it
        Then it should return an empty list
        """
        results = get_user_accessible_transferring_bodies(
            [
                "/something_else/test body1",
                "/something_else/test body2",
                "/ayr_user_type/bar",
            ]
        )
        assert results == []

    def test_transferring_bodies_in_groups_returns_corresponding_body_names(
        self, client: FlaskClient
    ):
        """
        Given a list of groups including 2 prefixed with
            /transferring_body_user/
            and another group
            and 2 corresponding bodies in the database
            and an extra body in the database
        When get_user_accessible_transferring_bodies is called with it
        Then it should return a list with the 2 corresponding body names
        """
        BodyFactory(Name="test body1")
        BodyFactory(Name="test body2")
        BodyFactory(Name="test body3")

        results = get_user_accessible_transferring_bodies(
            [
                "/transferring_body_user/test body1",
                "/transferring_body_user/test body2",
                "/foo/bar",
            ]
        )
        assert results == ["test body1", "test body2"]