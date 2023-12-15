from django.test import TestCase
from apps.authentication.dao import UserDAO, UserProfileDAO
from apps.authentication.dto import UserDTO
from apps.authentication.models import User, UserProfile

from parameterized import parameterized, param


class UserDAOTestCase(TestCase):

    def setUp(self):

        self._user_dao = UserDAO()

    def test_create_user(self):
        email = 'test@test.com'
        username = 'username'

        self._user_dao.create_user(UserDTO(email=email, username=username, password='password'))

        user = User.objects.get(email=email)
        userprofile = UserProfile.objects.get(user__email=email)

        self.assertEqual(username, user.username)
        self.assertEqual(username, userprofile.user.username)


class UserProfileDAOTestCase(TestCase):

    def setUp(self):
        self._userprofile_dao = UserProfileDAO()
        self._expected_user = UserProfile.objects.create(
            user_id=User.objects.create_user(username='test_username').id
        )

    @parameterized.expand(
        [
            param('test_username', True),
            param('test_username_2', False),
        ],
    )
    def test_is_user_exists(self, username, expected_result):
        result = self._userprofile_dao.is_user_exists(username)

        self.assertEqual(result, expected_result)
