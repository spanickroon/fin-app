import logging
from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django_otp import devices_for_user
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.authentication.dao import UserDAO, UserProfileDAO
from apps.authentication.dto import AuthServiceDTO, OTPUserDTO, UserDTO
from apps.authentication.forms import AuthUserForm, OTPAuthUserForm


class RegistrationUserService:
    _invalid_form_data_msg = "Invalid from data"
    _user_already_exists_msg = "User already exists"
    _register_msg = "Success registration"

    def __init__(self, user_dao: UserDAO, user_profile_dao: UserProfileDAO):
        self._user_dao = user_dao
        self._user_profile_dao = user_profile_dao

    def execute(
        self, request: HttpRequest, user_form_data: AuthUserForm
    ) -> AuthServiceDTO:
        if not user_form_data.is_valid():
            return AuthServiceDTO(
                status=HTTPStatus.BAD_REQUEST,
                message=f"{self._invalid_form_data_msg}, {user_form_data.errors}",
            )
        user = UserDTO(
            email=user_form_data.cleaned_data["email"],
            username=user_form_data.cleaned_data["username"],
            password=user_form_data.cleaned_data["password"],
        )
        if self._user_profile_dao.is_user_exists(user.username):
            return AuthServiceDTO(
                status=HTTPStatus.BAD_REQUEST, message=self._user_already_exists_msg
            )

        user_profile = self._user_dao.create_user(user)

        otp_user_service.execute(user_profile.user, state=otp_user_service.register)

        return AuthServiceDTO(status=HTTPStatus.CREATED, message=self._register_msg)


class LoginUserService:
    _invalid_form_data_msg = "Invalid from data"
    _user_not_found_msg = "User not found"
    _invalid_username_or_password = "Invalid username or password"
    _invalid_otp = "Invalid OTP code"
    _login_msg = "Success login"

    def __init__(self, user_dao: UserDAO, user_profile_dao: UserProfileDAO):
        self._user_dao = user_dao
        self._user_profile_dao = user_profile_dao

    def execute(
        self, request: HttpRequest, user_form_data: OTPAuthUserForm
    ) -> AuthServiceDTO:
        if not user_form_data.is_valid():
            return AuthServiceDTO(
                status=HTTPStatus.BAD_REQUEST,
                message=f"{self._invalid_form_data_msg}, {user_form_data.errors}",
            )

        otp_user = OTPUserDTO(
            email=user_form_data.cleaned_data["email"],
            username=user_form_data.cleaned_data["username"],
            password=user_form_data.cleaned_data["password"],
            otp=user_form_data.cleaned_data["otp"],
        )

        if not self._user_profile_dao.is_user_exists(otp_user.username):
            return AuthServiceDTO(
                status=HTTPStatus.NOT_FOUND, message=self._user_not_found_msg
            )

        user = authenticate(username=otp_user.username, password=otp_user.password)
        if not user:
            return AuthServiceDTO(
                status=HTTPStatus.NOT_FOUND, message=self._invalid_username_or_password
            )

        logging.info(user)
        if not otp_user_service.execute(
            user, state=otp_user_service.login, otp=otp_user.otp
        ):
            return AuthServiceDTO(
                status=HTTPStatus.NOT_FOUND, message=self._invalid_otp
            )

        login(request, user)

        return AuthServiceDTO(status=HTTPStatus.OK, message=self._login_msg)


class LogoutUserService:
    _logout_msg = "Success logout"

    def execute(self, request: HttpRequest) -> AuthServiceDTO:
        logout(request)
        return AuthServiceDTO(status=HTTPStatus.OK, message=self._logout_msg)


class OTPUserService:
    login = "login"
    register = "register"

    def execute(self, user, state: str, otp=None) -> bool:
        if state == self.register:
            self._send_email(user)
        else:
            return self._check_otp(user, otp)

    def _send_email(self, user) -> None:
        device = user.totpdevice_set.create(confirmed=True)

        message = render_to_string(
            "authentication/email_message.html",
            {
                "user": user,
                "qr_code": device.config_url,
            },
        )

        email = EmailMessage("Confirm registration", message, to=[user.email])
        email.content_subtype = "html"
        email.send()

    def _check_otp(self, user, otp) -> bool:
        device = self._get_device(user)
        is_match = totp(device.bin_key) == int(otp)

        logging.info(f"{user} otp is match: {is_match}")
        return is_match

    def _get_device(self, user):
        devices = devices_for_user(user, confirmed=True)
        for device in devices:
            if isinstance(device, TOTPDevice):
                return device


registration_user_service = RegistrationUserService(
    user_dao=UserDAO(), user_profile_dao=UserProfileDAO()
)
login_user_service = LoginUserService(
    user_dao=UserDAO(), user_profile_dao=UserProfileDAO()
)
logout_user_service = LogoutUserService()
otp_user_service = OTPUserService()
