from unittest.mock import Mock, patch

from http import HTTPStatus
from django.test import TestCase
from apps.authentication.services import registration_user_service, login_user_service
from apps.authentication.models import User, UserProfile
from apps.authentication.forms import AuthUserForm

from parameterized import parameterized, param


class RegistrationUserServiceTestCase(TestCase):

    def setUp(self):
        self._test_user = UserProfile.objects.create(
            user_id=User.objects.create_user(username='test_user').id
        )
        self._registration_user_service = registration_user_service
        self._auth_form = AuthUserForm()

    @parameterized.expand(
        [
            param({}, False, HTTPStatus.BAD_REQUEST, None),
            param({
                'email': 'test_user@test.com',
                'username': 'test_user',
                'password': '123123',
            }, False, HTTPStatus.BAD_REQUEST, None),
            param({
                'email': 'test_user_new@test.com',
                'username': 'test_user_new',
                'password': '123123',
            }, True, HTTPStatus.CREATED, 'test_user_new'),
        ]
    )
    @patch('apps.authentication.services.AuthUserForm')
    def test_execute(self, auth_form_data, is_valid, expected_status_code, expected_username, mock_form):
        mock_form.is_valid.return_value = is_valid
        mock_form.cleaned_data = auth_form_data
        result = self._registration_user_service.execute(Mock(), mock_form)

        self.assertEqual(result.status, expected_status_code)

        if expected_username:
            self.assertTrue(UserProfile.objects.filter(user__username=auth_form_data['username']).exists())


class LoginUserServiceTestCase(TestCase):

    def setUp(self):
        self._test_user = UserProfile.objects.create(
            user_id=User.objects.create_user(username='test_user', password='123123').id
        )
        self._login_user_service = login_user_service
        self._auth_form = AuthUserForm()

    @parameterized.expand(
        [
            param({}, False, HTTPStatus.BAD_REQUEST),
            param({
                'email': 'test_user@test.com',
                'username': 'test_user',
                'password': '123123',
                'otp': '123123',
            }, False, HTTPStatus.BAD_REQUEST),
            param({
                'email': 'test_user_new@test.com',
                'username': 'test_user_new',
                'password': '123123',
                'otp': '123123',
            }, True, HTTPStatus.NOT_FOUND),
            param({
                'email': 'test_user@test.com',
                'username': 'test_user',
                'password': '123123333',
                'otp': '123123',
            }, True, HTTPStatus.NOT_FOUND),
            param({
                'email': 'test_user@test.com',
                'username': 'test_user',
                'password': '123123',
                'otp': '123123',
            }, True, HTTPStatus.OK),
        ]
    )
    @patch('apps.authentication.services.OTPAuthUserForm')
    @patch('apps.authentication.services.otp_user_service')
    @patch('apps.authentication.services.login')
    def test_execute(self, auth_form_data, is_valid, expected_status_code, mock_form, mock_service, mock_login):
        mock_form.is_valid.return_value = is_valid
        mock_form.cleaned_data = auth_form_data

        result = self._login_user_service.execute(Mock(), mock_form)

        self.assertEqual(result.status, expected_status_code)
